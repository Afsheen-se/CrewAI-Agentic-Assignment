from crewai import Agent, Task
from google_sheets_manager import GoogleSheetsManager
from email_service import EmailService
from config import FINAL_SELECTION_COUNT, VOICE_PASSING_MARKS

class FinalizerAgent:
    def __init__(self):
        self.sheets_manager = GoogleSheetsManager()
        self.email_service = EmailService()
    
    def create_agent(self):
        """Create the Finalizer Agent"""
        return Agent(
            role='Finalizer',
            goal='Analyze quiz scores and video transcripts to select the top 5 students',
            backstory="""You are a senior selection committee member with expertise in evaluating 
            candidates based on multiple criteria. You excel at analyzing both quantitative scores 
            and qualitative content to make fair, informed decisions about candidate selection.""",
            verbose=True,
            allow_delegation=False
        )
    
    def finalize_selection(self):
        """Analyze scores and transcripts to select top 5 students"""
        try:
            # Get student data with quiz scores
            student_data = self.sheets_manager.get_student_data()
            
            # Get voice data with transcripts and scores
            voice_data = self.sheets_manager.read_data('Voice Submissions', 'A:E')
            
            # Combine data and calculate final scores
            combined_data = self._combine_student_data(student_data, voice_data)
            
            # Filter students who meet voice passing criteria (7+ marks)
            eligible_students = [s for s in combined_data if s['voice_score'] >= VOICE_PASSING_MARKS]
            
            if not eligible_students:
                print("No students meet the voice passing criteria!")
                return []
            
            # Sort eligible students by total score
            sorted_students = sorted(eligible_students, key=lambda x: x['total_score'], reverse=True)
            
            # Select top 5 from eligible students
            top_5_students = sorted_students[:FINAL_SELECTION_COUNT]
            
            print(f"Found {len(eligible_students)} students who meet video criteria")
            print(f"Selected top {len(top_5_students)} students for final selection")
            
            # Send final selection emails
            self._send_final_selection_emails(top_5_students)
            
            # Store final results
            self._store_final_results(combined_data, top_5_students)
            
            return top_5_students
            
        except Exception as e:
            print(f"Error finalizing selection: {e}")
            return []
    
    def _combine_student_data(self, student_data, voice_data):
        """Combine quiz scores with voice data"""
        try:
            combined_data = []
            
            # Create a mapping of student names to voice data
            voice_dict = {}
            for row in voice_data[1:]:  # Skip header
                if len(row) >= 5:
                    voice_dict[row[0]] = {
                        'voice_link': row[2],
                        'transcript': row[3],
                        'voice_score': int(row[4]) if row[4].isdigit() else 0
                    }
            
            # Combine student data with voice data
            for student in student_data:
                student_name = student['name']
                voice_info = voice_dict.get(student_name, {})
                
                # Calculate total score (quiz score + voice score, both out of 10)
                quiz_score = student['marks']  # Out of 10
                voice_score = voice_info.get('voice_score', 0)  # Out of 10
                total_score = (quiz_score + voice_score) / 2  # Average of both scores
                
                combined_student = {
                    'name': student_name,
                    'email': student['email'],
                    'quiz_score': quiz_score,
                    'voice_score': voice_score,
                    'total_score': total_score,
                    'voice_link': voice_info.get('voice_link', ''),
                    'transcript': voice_info.get('transcript', ''),
                    'final_status': 'Selected' if total_score >= 0 else 'Not Selected'
                }
                
                combined_data.append(combined_student)
            
            return combined_data
            
        except Exception as e:
            print(f"Error combining student data: {e}")
            return []
    
    def _send_final_selection_emails(self, top_5_students):
        """Send final selection emails to top 5 students"""
        try:
            email_results = []
            
            for student in top_5_students:
                success = self.email_service.send_final_selection_email(
                    student['email'],
                    student['name']
                )
                
                email_results.append({
                    'name': student['name'],
                    'email': student['email'],
                    'total_score': student['total_score'],
                    'email_sent': success
                })
            
            print(f"Sent final selection emails to {len(email_results)} students")
            return email_results
            
        except Exception as e:
            print(f"Error sending final selection emails: {e}")
            return []
    
    def _store_final_results(self, all_students, top_5_students):
        """Store final results in Google Sheets"""
        try:
            # Prepare data for Final Results sheet
            results_data = []
            
            for student in all_students:
                # Mark as selected if in top 5
                if student in top_5_students:
                    student['final_status'] = 'Selected'
                else:
                    student['final_status'] = 'Not Selected'
                
                row = [
                    student['name'],
                    student['email'],
                    student['quiz_score'],
                    student['video_score'],
                    student['total_score'],
                    student['final_status']
                ]
                results_data.append(row)
            
            # Write to Final Results sheet
            self.sheets_manager.write_data('Final Results', results_data, 'A1')
            
            print(f"Stored final results for {len(results_data)} students")
            
        except Exception as e:
            print(f"Error storing final results: {e}")
    
    def get_final_results(self):
        """Get final results from Google Sheets"""
        return self.sheets_manager.get_final_results()
    
    def create_task(self):
        """Create a task for the Finalizer Agent"""
        return Task(
            description="Analyze quiz scores and video transcripts to select the top 5 students",
            expected_output="List of top 5 selected students with final selection emails sent",
            agent=self.create_agent()
        )
