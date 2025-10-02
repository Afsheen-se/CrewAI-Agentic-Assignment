from crewai import Agent, Task
from google_sheets_manager import GoogleSheetsManager
from config import QUIZ_PASSING_MARKS
import json

class QuizCheckerAgent:
    def __init__(self):
        self.sheets_manager = GoogleSheetsManager()
    
    def create_agent(self):
        """Create the Quiz Checker Agent"""
        return Agent(
            role='Quiz Checker',
            goal='Accurately check student quiz responses and calculate scores',
            backstory="""You are an experienced educational assessor with expertise in evaluating 
            student responses and providing fair, accurate scoring. You have a keen eye for detail 
            and ensure that all student responses are evaluated consistently and fairly.""",
            verbose=True,
            allow_delegation=False
        )
    
    def check_quiz_responses(self, student_responses):
        """Check student quiz responses and calculate scores"""
        try:
            # Get quiz questions from Google Sheets
            questions = self.sheets_manager.get_quiz_questions()
            
            if not questions:
                print("No quiz questions found in Google Sheets")
                return []
            
            results = []
            
            for student_data in student_responses:
                student_name = student_data.get('name', '')
                student_email = student_data.get('email', '')
                responses = student_data.get('responses', [])
                
                # Calculate score
                score = self._calculate_score(questions, responses)
                
                # Determine pass/fail status
                passed = score >= QUIZ_PASSING_MARKS
                status = "PASSED" if passed else "FAILED"
                
                # Store student data
                student_result = {
                    'name': student_name,
                    'email': student_email,
                    'marks': score,
                    'responses': json.dumps(responses) if responses else '',
                    'status': status,
                    'passed': passed
                }
                
                results.append(student_result)
                
                # Store in Google Sheets
                self._store_student_result(student_result)
            
            return results
            
        except Exception as e:
            print(f"Error checking quiz responses: {e}")
            return []
    
    def _calculate_score(self, questions, student_responses):
        """Calculate score based on correct answers"""
        try:
            if not student_responses or len(student_responses) != len(questions):
                return 0
            
            correct_count = 0
            total_questions = len(questions)
            
            for i, question in enumerate(questions):
                if i < len(student_responses):
                    student_answer = student_responses[i].upper().strip()
                    correct_answer = question['correct_answer'].upper().strip()
                    
                    if student_answer == correct_answer:
                        correct_count += 1
            
            # Return raw score (number of correct answers out of total)
            return correct_count
            
        except Exception as e:
            print(f"Error calculating score: {e}")
            return 0
    
    def _store_student_result(self, student_result):
        """Store student result in Google Sheets"""
        try:
            row_data = [
                student_result['name'],
                student_result['email'],
                student_result['marks'],
                student_result['responses'],
                student_result['status']
            ]
            
            self.sheets_manager.append_data('Student Data', [row_data])
            
        except Exception as e:
            print(f"Error storing student result: {e}")
    
    def get_student_scores(self):
        """Get all student scores from Google Sheets"""
        return self.sheets_manager.get_student_data()
    
    def create_task(self, student_responses):
        """Create a task for the Quiz Checker Agent"""
        return Task(
            description="Check student quiz responses and calculate accurate scores",
            expected_output="List of student scores and detailed feedback",
            agent=self.create_agent()
        )
