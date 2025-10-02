import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import (
    EMAIL_SMTP_SERVER,
    EMAIL_SMTP_PORT,
    EMAIL_USERNAME,
    EMAIL_PASSWORD,
    FROM_EMAIL
)

class EmailService:
    def __init__(self):
        self.smtp_server = EMAIL_SMTP_SERVER
        self.smtp_port = EMAIL_SMTP_PORT
        self.username = EMAIL_USERNAME
        self.password = EMAIL_PASSWORD
        self.from_email = FROM_EMAIL
    
    def send_email(self, to_email, subject, body, is_html=False):
        """Send an email to a recipient"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add body
            if is_html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))
            
            # Connect to server and send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            text = msg.as_string()
            server.sendmail(self.from_email, to_email, text)
            server.quit()
            
            print(f"Email sent successfully to {to_email}")
            return True
        except Exception as e:
            print(f"Error sending email to {to_email}: {e}")
            return False
    
    def send_quiz_invitation(self, student_email, student_name, quiz_link):
        """Send quiz invitation email to student"""
        subject = "Quiz Invitation - AISB Onboarding Process"
        
        body = f"""
Dear {student_name},

Congratulations! You have been selected to participate in the AISB Onboarding Process quiz.

Please click the following link to take the quiz:
{quiz_link}

Instructions:
- You have 30 minutes to complete the quiz
- The quiz consists of multiple-choice questions
- Answer all questions to the best of your ability
- Your responses will be automatically saved

Good luck!

Best regards,
AISB Team
        """
        
        return self.send_email(student_email, subject, body)
    
    def send_voice_submission_invitation(self, student_email, student_name):
        """Send voice submission invitation to students who passed the quiz"""
        subject = "🎵 Voice Submission Required - AISB Onboarding Process"
        
        body = f"""
Dear {student_name},

🎉 Congratulations! You have successfully passed the quiz with 7+ marks and are now invited to submit a voice recording for the next stage of the AISB Onboarding Process.

🎙️ Voice Recording Instructions:
1. Record a 1-minute audio introduction of yourself
2. Explain your background and passion for AI/Data Science
3. Share your career goals and why you want to join this bootcamp
4. Save as MP3, M4A, or WAV format
5. Upload the audio file to Google Drive
6. Share the file with "Anyone with link can view" permissions
7. Submit the Google Drive link through our system

📱 Recording Tips:
- Use your phone's voice recorder app
- Find a quiet location with minimal background noise
- Speak clearly and at a moderate pace
- Keep it to exactly 1 minute
- Show enthusiasm and professionalism

⏰ Deadline: Submit within 3 days of receiving this email

Your audio will be automatically transcribed and analyzed by our AI system for final selection.

Best regards,
AISB Team
        """
        
        return self.send_email(student_email, subject, body)
    
    def send_final_selection_email(self, student_email, student_name):
        """Send final selection email to selected students"""
        subject = "🎉 Congratulations! You've been selected for AI Bootcamp at AI Skillbridge"
        
        body = f"""
Dear {student_name},

🎉 CONGRATULATIONS! 🎉

You have been successfully selected to join the AI Bootcamp at AI Skillbridge!

Your outstanding performance in both the quiz and video submission has earned you a place in our prestigious program. We were particularly impressed by:
- Your excellent quiz performance
- The quality and clarity of your video submission
- Your overall presentation and communication skills
- Your passion for AI and Data Science

🏆 What's Next:
- You will receive detailed instructions about the AI Bootcamp program
- Please check your email regularly for updates and next steps
- Welcome to the AI Skillbridge community!

We are excited to have you join us and look forward to your contributions to the AI Bootcamp.

Best regards,
AI Skillbridge Team
aisb-onboarding-service@aisb-onboarding-process.iam.gserviceaccount.com
        """
        
        return self.send_email(student_email, subject, body)
    
    def send_bulk_emails(self, email_list, email_type, **kwargs):
        """Send bulk emails to a list of recipients"""
        results = []
        
        for email_data in email_list:
            if email_type == 'quiz_invitation':
                result = self.send_quiz_invitation(
                    email_data['email'], 
                    email_data['name'], 
                    kwargs.get('quiz_link', '')
                )
            elif email_type == 'voice_submission':
                result = self.send_voice_submission_invitation(
                    email_data['email'], 
                    email_data['name']
                )
            elif email_type == 'final_selection':
                result = self.send_final_selection_email(
                    email_data['email'], 
                    email_data['name']
                )
            else:
                result = False
            
            results.append({
                'email': email_data['email'],
                'name': email_data['name'],
                'success': result
            })
        
        return results
