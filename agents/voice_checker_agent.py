from crewai import Agent, Task
from google_sheets_manager import GoogleSheetsManager
from voice_processor import VoiceProcessor

class VoiceCheckerAgent:
    def __init__(self):
        self.sheets_manager = GoogleSheetsManager()
        self.voice_processor = VoiceProcessor()
    
    def create_agent(self):
        """Create the Voice Checker Agent"""
        return Agent(
            role='Voice Checker & Transcript Generator',
            goal='Process voice submissions and generate accurate transcripts',
            backstory="""You are an audio content specialist with expertise in voice analysis 
            and transcription. You have advanced skills in processing various audio formats and 
            generating accurate, detailed transcripts that capture the essence of spoken content.""",
            verbose=True,
            allow_delegation=False
        )
    
    def process_voice_submissions(self, voice_submissions):
        """Process voice submissions and generate transcripts"""
        try:
            results = []
            
            for submission in voice_submissions:
                student_name = submission.get('student_name', '')
                voice_link = submission.get('voice_link', '') or submission.get('video_link', '')  # Support both keys
                
                if not student_name or not voice_link:
                    print(f"Missing data for submission: {submission}")
                    continue
                
                print(f"Processing voice submission for {student_name}")
                
                # Process the voice submission
                result = self.voice_processor.process_audio_submission(student_name, voice_link)
                
                if result:
                    # Store in Google Sheets
                    self._store_voice_result(result)
                    results.append(result)
                    print(f"✅ Processed voice for {student_name}: Score {result['score']}/10")
                else:
                    print(f"❌ Failed to process voice for {student_name}")
            
            return {
                'status': 'completed',
                'processed_voices': results,
                'message': f'Successfully processed {len(results)} voice submissions'
            }
            
        except Exception as e:
            print(f"Error in voice processing: {e}")
            return {
                'status': 'error',
                'message': f'Voice processing failed: {str(e)}'
            }
    
    def _store_voice_result(self, result):
        """Store voice processing result in Google Sheets"""
        try:
            # Prepare data for Voice Submissions sheet
            row_data = [
                result['student_name'],
                result['audio_link'],  # This will be the voice link
                result['transcript'][:500] + '...' if len(result['transcript']) > 500 else result['transcript'],
                result['score'],
                result['analysis'][:200] + '...' if len(result['analysis']) > 200 else result['analysis']
            ]
            
            # Append to Voice Submissions sheet
            self.sheets_manager.append_data('Voice Submissions', [row_data])
            
            print(f"✅ Stored voice result for {result['student_name']}")
            
        except Exception as e:
            print(f"❌ Error storing voice result: {e}")
    
    def create_task(self, voice_submissions):
        """Create a task for processing voice submissions"""
        return Task(
            description=f"""
            Process {len(voice_submissions)} voice submissions:
            
            For each voice submission:
            1. Extract and validate the Google Drive voice link
            2. Generate accurate transcript of the 1-minute audio introduction
            3. Analyze the content for:
               - Clarity of communication
               - Professional presentation
               - Relevance to AI/Data Science
               - Enthusiasm and engagement
            4. Provide a score from 1-10
            5. Store results in Google Sheets
            
            Voice submissions to process:
            {[f"- {s.get('student_name', 'Unknown')}: {s.get('voice_link', s.get('video_link', 'No link'))}" for s in voice_submissions]}
            
            Ensure all transcripts are accurate and analysis is thorough.
            """,
            agent=self.create_agent(),
            expected_output="Detailed processing results with transcripts, analysis, and scores for all voice submissions"
        )
    
    def run_voice_processing_only(self, voice_submissions):
        """Run only voice processing without full workflow"""
        try:
            print(f"🎵 Processing {len(voice_submissions)} voice submissions...")
            
            # Process voice submissions
            result = self.process_voice_submissions(voice_submissions)
            
            if result['status'] == 'completed':
                print(f"✅ Voice processing completed: {result['message']}")
            else:
                print(f"❌ Voice processing failed: {result['message']}")
            
            return result
            
        except Exception as e:
            print(f"❌ Error in voice processing workflow: {e}")
            return {
                'status': 'error',
                'message': f'Voice processing workflow failed: {str(e)}'
            }
    
    def get_voice_submissions(self):
        """Get voice submissions from Google Sheets"""
        try:
            voice_data = self.sheets_manager.read_data('Voice Submissions', 'A:E')
            if len(voice_data) <= 1:  # Only headers or empty
                return []
            
            submissions = []
            for row in voice_data[1:]:  # Skip header
                if len(row) >= 5:
                    submissions.append({
                        'student_name': row[0],
                        'voice_link': row[1],
                        'transcript': row[2],
                        'score': row[3],
                        'analysis': row[4]
                    })
            
            return submissions
            
        except Exception as e:
            print(f"Error getting voice submissions: {e}")
            return []
