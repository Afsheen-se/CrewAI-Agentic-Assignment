import os
from dotenv import load_dotenv

load_dotenv()

# Google Sheets Configuration
GOOGLE_SHEETS_CREDENTIALS_FILE = os.getenv('GOOGLE_SHEETS_CREDENTIALS_FILE', 'credentials.json')
GOOGLE_SHEET_ID = os.getenv('GOOGLE_SHEET_ID', '')
GOOGLE_SHEET_QUIZ_QUESTIONS = 'Quiz Questions'
GOOGLE_SHEET_STUDENT_DATA = 'Student Data'
GOOGLE_SHEET_VOICE_SUBMISSIONS = 'Voice Submissions'
GOOGLE_SHEET_FINAL_RESULTS = 'Final Results'

# OpenAI API Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')

# Email Configuration
EMAIL_SMTP_SERVER = os.getenv('EMAIL_SMTP_SERVER', 'smtp.gmail.com')
EMAIL_SMTP_PORT = int(os.getenv('EMAIL_SMTP_PORT', '587'))
EMAIL_USERNAME = os.getenv('EMAIL_USERNAME', '')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
FROM_EMAIL = os.getenv('FROM_EMAIL', '')

# Application Configuration
TOP_STUDENTS_COUNT = 10
FINAL_SELECTION_COUNT = 5
QUIZ_QUESTIONS_COUNT = 10

# Passing Criteria
QUIZ_PASSING_MARKS = 7  # Out of 10 questions (70%)
VOICE_PASSING_MARKS = 7  # Out of 10 marks (70%)
