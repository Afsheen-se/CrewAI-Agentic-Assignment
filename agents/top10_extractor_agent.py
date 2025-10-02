from crewai import Agent, Task
from google_sheets_manager import GoogleSheetsManager
from email_service import EmailService
from config import TOP_STUDENTS_COUNT

class Top10ExtractorAgent:
    def __init__(self):
        self.sheets_manager = GoogleSheetsManager()
        self.email_service = EmailService()
    
    def create_agent(self):
        """Create the Top 10 Extractor Agent"""
        return Agent(
            role='Top 10 Extractor',
            goal='Identify top performing students and send them video submission invitations',
            backstory="""You are a recruitment specialist with expertise in identifying top talent 
            and managing communication with high-performing candidates. You excel at analyzing 
            performance data and ensuring that the best candidates receive appropriate recognition 
            and next steps in the selection process.""",
            verbose=True,
            allow_delegation=False
        )
    
    def extract_top_students(self):
        """Extract top 10 students who PASSED the quiz"""
        try:
            # Get all student data
            all_students = self.sheets_manager.get_student_data()
            
            if not all_students:
                print("No student data found")
                return []
            
            # Filter only students who PASSED the quiz
            passed_students = [s for s in all_students if s.get('status') == 'PASSED' or s.get('passed', False)]
            
            print(f"Debug: Found {len(all_students)} total students")
            for student in all_students:
                print(f"Debug: {student.get('name')} - Status: {student.get('status')} - Marks: {student.get('marks')}")
            
            if not passed_students:
                print("No students passed the quiz!")
                return []
            
            # Sort passed students by marks (descending)
            sorted_students = sorted(passed_students, key=lambda x: x['marks'], reverse=True)
            
            # Get top 10 students who passed
            top_students = sorted_students[:TOP_STUDENTS_COUNT]
            
            print(f"Found {len(passed_students)} students who passed the quiz")
            print(f"Selected top {len(top_students)} students for video submission")
            
            # Send email invitations only to students who passed
            email_results = self._send_video_invitations(top_students)
            
            print(f"Debug: Email sending results: {email_results}")
            
            return top_students
            
        except Exception as e:
            print(f"Error extracting top students: {e}")
            return []
    
    def _send_video_invitations(self, top_students):
        """Send voice submission invitations to top students"""
        try:
            email_results = []
            
            for student in top_students:
                print(f"Debug: Sending voice invitation to {student['name']} ({student['email']})")
                success = self.email_service.send_voice_submission_invitation(
                    student['email'],
                    student['name']
                )
                print(f"Debug: Email sent to {student['name']}: {success}")
                
                email_results.append({
                    'name': student['name'],
                    'email': student['email'],
                    'marks': student['marks'],
                    'email_sent': success
                })
            
            # Store results in Google Sheets
            self._store_top_students_data(email_results)
            
            return email_results
            
        except Exception as e:
            print(f"Error sending video invitations: {e}")
            return []
    
    def _store_top_students_data(self, top_students_data):
        """Store top students data in Google Sheets"""
        try:
            # Prepare data for Voice Submissions sheet
            voice_submissions_data = []
            for student in top_students_data:
                row = [
                    student['name'],
                    student['email'],
                    '',  # Voice Link (to be filled later)
                    '',  # Transcript (to be filled later)
                    ''   # Voice Score (to be filled later)
                ]
                voice_submissions_data.append(row)
            
            # Write to Voice Submissions sheet
            self.sheets_manager.write_data(
                'Voice Submissions',
                voice_submissions_data,
                'A2'  # Start from row 2 (after headers)
            )
            
            print(f"Stored {len(top_students_data)} top students in Voice Submissions sheet")
            
        except Exception as e:
            print(f"Error storing top students data: {e}")
    
    def get_top_students(self):
        """Get top students from Google Sheets"""
        return self.sheets_manager.get_top_students(TOP_STUDENTS_COUNT)
    
    def create_task(self):
        """Create a task for the Top 10 Extractor Agent"""
        return Task(
            description="Extract top 10 students based on quiz scores and send them video submission invitations",
            expected_output="List of top 10 students with email invitations sent",
            agent=self.create_agent()
        )
