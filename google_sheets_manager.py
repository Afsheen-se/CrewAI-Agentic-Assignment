import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import json
from config import (
    GOOGLE_SHEETS_CREDENTIALS_FILE,
    GOOGLE_SHEET_ID,
    GOOGLE_SHEET_QUIZ_QUESTIONS,
    GOOGLE_SHEET_STUDENT_DATA,
    GOOGLE_SHEET_VOICE_SUBMISSIONS,
    GOOGLE_SHEET_FINAL_RESULTS
)

class GoogleSheetsManager:
    def __init__(self):
        self.credentials = None
        self.service = None
        self.sheet_id = GOOGLE_SHEET_ID
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Sheets API"""
        try:
            # Define the scope
            scope = ['https://www.googleapis.com/auth/spreadsheets']
            
            # Load credentials from file
            self.credentials = Credentials.from_service_account_file(
                GOOGLE_SHEETS_CREDENTIALS_FILE, scopes=scope
            )
            
            # Build the service
            self.service = build('sheets', 'v4', credentials=self.credentials)
            print("Successfully authenticated with Google Sheets API")
        except Exception as e:
            print(f"Error authenticating with Google Sheets: {e}")
            raise
    
    def create_sheets_if_not_exist(self):
        """Create the required sheets if they don't exist"""
        try:
            # Get existing sheets
            sheet_metadata = self.service.spreadsheets().get(spreadsheetId=self.sheet_id).execute()
            existing_sheets = [sheet['properties']['title'] for sheet in sheet_metadata['sheets']]
            
            sheets_to_create = [
                GOOGLE_SHEET_QUIZ_QUESTIONS,
                GOOGLE_SHEET_STUDENT_DATA,
                GOOGLE_SHEET_VOICE_SUBMISSIONS,
                GOOGLE_SHEET_FINAL_RESULTS
            ]
            
            for sheet_name in sheets_to_create:
                if sheet_name not in existing_sheets:
                    self._create_sheet(sheet_name)
                    self._setup_sheet_headers(sheet_name)
            
            print("All required sheets created/verified")
        except Exception as e:
            print(f"Error creating sheets: {e}")
            raise
    
    def _create_sheet(self, sheet_name):
        """Create a new sheet"""
        request_body = {
            'requests': [{
                'addSheet': {
                    'properties': {
                        'title': sheet_name
                    }
                }
            }]
        }
        
        self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.sheet_id,
            body=request_body
        ).execute()
    
    def _setup_sheet_headers(self, sheet_name):
        """Setup headers for each sheet"""
        headers = {
            GOOGLE_SHEET_QUIZ_QUESTIONS: ['Question', 'Option 1', 'Option 2', 'Option 3', 'Option 4', 'Correct Answer'],
            GOOGLE_SHEET_STUDENT_DATA: ['Name', 'Email', 'Quiz Marks', 'Quiz Responses', 'Status'],
            GOOGLE_SHEET_VOICE_SUBMISSIONS: ['Student Name', 'Email', 'Voice Link', 'Transcript', 'Voice Score'],
            GOOGLE_SHEET_FINAL_RESULTS: ['Student Name', 'Email', 'Quiz Score', 'Voice Score', 'Total Score', 'Final Status']
        }
        
        if sheet_name in headers:
            self.write_data(sheet_name, [headers[sheet_name]], 'A1')
    
    def write_data(self, sheet_name, data, range_name):
        """Write data to a specific sheet and range"""
        try:
            body = {'values': data}
            result = self.service.spreadsheets().values().update(
                spreadsheetId=self.sheet_id,
                range=f"{sheet_name}!{range_name}",
                valueInputOption='RAW',
                body=body
            ).execute()
            return result
        except Exception as e:
            print(f"Error writing data to {sheet_name}: {e}")
            raise
    
    def read_data(self, sheet_name, range_name):
        """Read data from a specific sheet and range"""
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.sheet_id,
                range=f"{sheet_name}!{range_name}"
            ).execute()
            return result.get('values', [])
        except Exception as e:
            print(f"Error reading data from {sheet_name}: {e}")
            return []
    
    def append_data(self, sheet_name, data):
        """Append data to a sheet"""
        try:
            body = {'values': data}
            result = self.service.spreadsheets().values().append(
                spreadsheetId=self.sheet_id,
                range=f"{sheet_name}!A:Z",
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()
            return result
        except Exception as e:
            print(f"Error appending data to {sheet_name}: {e}")
            raise
    
    def get_quiz_questions(self):
        """Get all quiz questions"""
        data = self.read_data(GOOGLE_SHEET_QUIZ_QUESTIONS, 'A:F')
        if len(data) <= 1:  # Only headers
            return []
        
        questions = []
        for row in data[1:]:  # Skip header
            if len(row) >= 6:
                questions.append({
                    'question': row[0],
                    'option1': row[1],
                    'option2': row[2],
                    'option3': row[3],
                    'option4': row[4],
                    'correct_answer': row[5]
                })
        return questions
    
    def get_student_data(self):
        """Get all student data"""
        data = self.read_data(GOOGLE_SHEET_STUDENT_DATA, 'A:E')  # Read 5 columns including Status
        if len(data) <= 1:  # Only headers
            return []
        
        students = []
        for row in data[1:]:  # Skip header
            if len(row) >= 3:
                students.append({
                    'name': row[0],
                    'email': row[1],
                    'marks': int(row[2]) if row[2].isdigit() else 0,
                    'responses': row[3] if len(row) > 3 else '',
                    'status': row[4] if len(row) > 4 else 'PENDING'
                })
        return students
    
    def get_top_students(self, count=10):
        """Get top students by marks"""
        students = self.get_student_data()
        sorted_students = sorted(students, key=lambda x: x['marks'], reverse=True)
        return sorted_students[:count]
    
    def get_final_results(self):
        """Get final results"""
        data = self.read_data(GOOGLE_SHEET_FINAL_RESULTS, 'A:F')
        if len(data) <= 1:  # Only headers
            return []
        
        results = []
        for row in data[1:]:  # Skip header
            if len(row) >= 6:
                results.append({
                    'name': row[0],
                    'email': row[1],
                    'quiz_score': int(row[2]) if row[2].isdigit() else 0,
                    'video_score': int(row[3]) if row[3].isdigit() else 0,
                    'total_score': int(row[4]) if row[4].isdigit() else 0,
                    'status': row[5]
                })
        return results
    
    def clear_sheet(self, sheet_name):
        """Clear all data from a specific sheet and reset headers"""
        try:
            # Get the sheet range
            range_name = f"{sheet_name}!A:Z"
            
            # Clear the sheet
            self.service.spreadsheets().values().clear(
                spreadsheetId=self.sheet_id,
                range=range_name
            ).execute()
            
            # Reset headers after clearing
            self._setup_sheet_headers(sheet_name)
            
            print(f"✅ Cleared sheet: {sheet_name}")
            return True
            
        except Exception as e:
            print(f"❌ Error clearing sheet {sheet_name}: {e}")
            return False
