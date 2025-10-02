import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse, parse_qs
from llm_manager import llm_manager

class VoiceProcessor:
    def __init__(self):
        self.llm = llm_manager.get_llm()
    
    def extract_file_id_from_drive_link(self, drive_link):
        """Extract file ID from Google Drive link (works for audio files)"""
        try:
            # Handle different Google Drive link formats
            if 'drive.google.com' in drive_link:
                if '/file/d/' in drive_link:
                    # Format: https://drive.google.com/file/d/FILE_ID/view
                    file_id = drive_link.split('/file/d/')[1].split('/')[0]
                elif 'id=' in drive_link:
                    # Format: https://drive.google.com/open?id=FILE_ID
                    file_id = parse_qs(urlparse(drive_link).query)['id'][0]
                else:
                    return None
                return file_id
            return None
        except Exception as e:
            print(f"Error extracting file ID: {e}")
            return None
    
    def get_audio_transcript_from_drive(self, drive_link):
        """Get transcript from Google Drive audio file"""
        try:
            # Check if this is a demo/mock link
            if 'ABC123DEF456' in drive_link or 'GHI789JKL012' in drive_link or 'MNO345PQR678' in drive_link:
                # Return realistic demo transcript
                demo_transcripts = {
                    'ABC123DEF456': """Hello, my name is John Smith. I'm passionate about artificial intelligence and machine learning. I have 3 years of experience working with Python and data analysis. I've completed several projects involving neural networks and deep learning. I'm particularly interested in natural language processing and computer vision. My goal is to become an AI researcher and contribute to cutting-edge solutions that can solve real-world problems. I believe this bootcamp will provide me with the advanced skills I need to achieve my career objectives.""",
                    
                    'GHI789JKL012': """Hi everyone, I'm Sarah Johnson. I've been working in data science for 2 years and I absolutely love solving complex problems using machine learning algorithms. I have experience with TensorFlow, PyTorch, and scikit-learn. I've worked on projects involving predictive analytics, recommendation systems, and time series forecasting. What excites me most about AI is its potential to transform industries and improve people's lives. I'm eager to learn more advanced techniques and collaborate with like-minded individuals in this bootcamp.""",
                    
                    'MNO345PQR678': """Hello, I'm Lisa Davis. I recently graduated with a degree in computer science and I'm excited to dive deeper into the world of artificial intelligence. During my studies, I worked on several machine learning projects and fell in love with the field. I have strong programming skills in Python and Java, and I'm familiar with data visualization tools like matplotlib and seaborn. I'm particularly interested in ethical AI and ensuring that AI systems are fair and unbiased. I see this bootcamp as the perfect opportunity to advance my skills and start my career in AI."""
                }
                
                # Return appropriate demo transcript
                for demo_id, transcript in demo_transcripts.items():
                    if demo_id in drive_link:
                        return transcript
                
                # Default demo transcript
                return "Hello, I'm excited to be part of this AI bootcamp. I have a strong background in programming and I'm passionate about machine learning and artificial intelligence."
            
            # For real links, attempt actual processing
            file_id = self.extract_file_id_from_drive_link(drive_link)
            if not file_id:
                return "Error: Could not extract file ID from link. Please ensure the link is a valid Google Drive audio link."
            
            # Simulate transcript generation for real links
            # In production, replace this with actual transcription service
            simulated_transcript = f"""
            This is a simulated transcript for audio file ID: {file_id}
            
            [Student Introduction]
            Hello, my name is [Student Name] and I'm excited to be part of the AISB Onboarding Process.
            
            [Background]
            I have a background in [field] and I'm passionate about artificial intelligence and data science.
            
            [Career Goals]
            My career goals include becoming a data scientist and contributing to AI research.
            
            [Closing]
            Thank you for considering my application. I look forward to the opportunity to work with AISB.
            """
            
            return simulated_transcript.strip()
            
        except Exception as e:
            print(f"Error getting transcript: {e}")
            return f"Error generating transcript: {str(e)}"
    
    def analyze_audio_content(self, transcript):
        """Analyze audio content using AI"""
        try:
            prompt = f"""
            Analyze the following audio transcript from a 1-minute student introduction and provide a score from 1-10 based on:
            1. Clarity of communication (1-3 points)
            2. Professional presentation (1-3 points)
            3. Content relevance to AI/Data Science (1-2 points)
            4. Enthusiasm and engagement (1-2 points)
            
            Transcript:
            {transcript}
            
            Please provide:
            1. A numerical score (1-10)
            2. Brief feedback on strengths
            3. Areas for improvement
            4. Overall assessment
            
            Format your response as:
            Score: [number]
            Strengths: [text]
            Improvements: [text]
            Assessment: [text]
            """
            
            # Use centralized LLM provider
            from llm_provider import MODEL
            
            response = MODEL.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"Error analyzing audio content: {e}")
            return f"Error analyzing content: {str(e)}"
    
    def extract_score_from_analysis(self, analysis_text):
        """Extract numerical score from analysis text"""
        try:
            # Look for "Score: [number]" pattern
            score_match = re.search(r'Score:\s*(\d+)', analysis_text)
            if score_match:
                return int(score_match.group(1))
            
            # Fallback: look for any number in the text
            numbers = re.findall(r'\d+', analysis_text)
            if numbers:
                return int(numbers[0])
            
            return 5  # Default score if no number found
            
        except Exception as e:
            print(f"Error extracting score: {e}")
            return 5
    
    def process_audio_submission(self, student_name, audio_link):
        """Process an audio submission and return analysis results"""
        try:
            # Get transcript
            transcript = self.get_audio_transcript_from_drive(audio_link)
            
            # Analyze content
            analysis = self.analyze_audio_content(transcript)
            
            # Extract score
            score = self.extract_score_from_analysis(analysis)
            
            return {
                'student_name': student_name,
                'audio_link': audio_link,
                'transcript': transcript,
                'analysis': analysis,
                'score': score
            }
            
        except Exception as e:
            print(f"Error processing audio submission: {e}")
            return {
                'student_name': student_name,
                'audio_link': audio_link,
                'transcript': f"Error: {str(e)}",
                'analysis': f"Error: {str(e)}",
                'score': 0
            }
