from crewai import Crew, Process
from agents.quiz_generator_agent import QuizGeneratorAgent
from agents.quiz_checker_agent import QuizCheckerAgent
from agents.top10_extractor_agent import Top10ExtractorAgent
from agents.voice_checker_agent import VoiceCheckerAgent
from agents.finalizer_agent import FinalizerAgent
from google_sheets_manager import GoogleSheetsManager
import time

class AISBOnboardingWorkflow:
    def __init__(self):
        self.quiz_generator = QuizGeneratorAgent()
        self.quiz_checker = QuizCheckerAgent()
        self.top10_extractor = Top10ExtractorAgent()
        self.voice_checker = VoiceCheckerAgent()
        self.finalizer = FinalizerAgent()
        self.sheets_manager = GoogleSheetsManager()
    
    def run_complete_workflow(self, topics, student_responses=None, voice_submissions=None):
        """Run the complete AISB onboarding workflow"""
        try:
            print("🚀 Starting AISB Onboarding Workflow...")
            
            # Step 1: Initialize Google Sheets
            print("\n📊 Setting up Google Sheets...")
            self.sheets_manager.create_sheets_if_not_exist()
            
            # Step 2: Generate Quiz Questions
            print("\n📝 Step 1: Generating Quiz Questions...")
            quiz_questions = self.quiz_generator.generate_quiz_questions(topics)
            print(f"✅ Generated {len(quiz_questions)} quiz questions")
            
            # Step 3: Check Quiz Responses (if provided)
            if student_responses:
                print("\n📊 Step 2: Checking Quiz Responses...")
                quiz_results = self.quiz_checker.check_quiz_responses(student_responses)
                print(f"✅ Processed {len(quiz_results)} student responses")
            else:
                print("\n⏳ Step 2: Waiting for student responses...")
                print("Please provide student responses to continue with the workflow")
                return {"status": "waiting_for_responses", "quiz_questions": quiz_questions}
            
            # Step 4: Extract Top 10 Students
            print("\n🏆 Step 3: Extracting Top 10 Students...")
            top_students = self.top10_extractor.extract_top_students()
            print(f"✅ Identified {len(top_students)} top students")
            
            # Step 5: Process Voice Submissions (if provided)
            if voice_submissions:
                print("\n🎵 Step 4: Processing Voice Submissions...")
                voice_results = self.voice_checker.process_voice_submissions(voice_submissions)
                print(f"✅ Processed {len(voice_results)} voice submissions")
            else:
                print("\n⏳ Step 4: Waiting for voice submissions...")
                print("Please provide voice submissions to continue with the workflow")
                return {
                    "status": "waiting_for_voices", 
                    "top_students": top_students,
                    "quiz_questions": quiz_questions
                }
            
            # Step 6: Finalize Selection
            print("\n🎯 Step 5: Finalizing Selection...")
            final_selection = self.finalizer.finalize_selection()
            print(f"✅ Selected {len(final_selection)} final students")
            
            # Return complete results
            return {
                "status": "completed",
                "quiz_questions": quiz_questions,
                "quiz_results": quiz_results,
                "top_students": top_students,
                "voice_results": voice_results,
                "final_selection": final_selection
            }
            
        except Exception as e:
            print(f"❌ Error in workflow: {e}")
            return {"status": "error", "message": str(e)}
    
    def run_quiz_generation_only(self, topics):
        """Run only the quiz generation step"""
        try:
            print("📝 Generating Quiz Questions...")
            self.sheets_manager.create_sheets_if_not_exist()
            quiz_questions = self.quiz_generator.generate_quiz_questions(topics)
            return {"status": "completed", "quiz_questions": quiz_questions}
        except Exception as e:
            print(f"❌ Error generating quiz: {e}")
            return {"status": "error", "message": str(e)}
    
    def run_quiz_checking_only(self, student_responses):
        """Run only the quiz checking step"""
        try:
            print("📊 Checking Quiz Responses...")
            quiz_results = self.quiz_checker.check_quiz_responses(student_responses)
            return {"status": "completed", "quiz_results": quiz_results}
        except Exception as e:
            print(f"❌ Error checking quiz: {e}")
            return {"status": "error", "message": str(e)}
    
    def run_top10_extraction_only(self):
        """Run only the top 10 extraction step"""
        try:
            print("🏆 Extracting Top 10 Students...")
            top_students = self.top10_extractor.extract_top_students()
            return {"status": "completed", "top_students": top_students}
        except Exception as e:
            print(f"❌ Error extracting top students: {e}")
            return {"status": "error", "message": str(e)}
    
    def run_video_processing_only(self, voice_submissions):
        """Run only the voice processing step (keeping method name for compatibility)"""
        try:
            print("🎵 Processing Voice Submissions...")
            voice_results = self.voice_checker.process_voice_submissions(voice_submissions)
            return {"status": "completed", "voice_results": voice_results}
        except Exception as e:
            print(f"❌ Error processing voices: {e}")
            return {"status": "error", "message": str(e)}
    
    def run_finalization_only(self):
        """Run only the finalization step"""
        try:
            print("🎯 Finalizing Selection...")
            final_selection = self.finalizer.finalize_selection()
            return {"status": "completed", "final_selection": final_selection}
        except Exception as e:
            print(f"❌ Error finalizing selection: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_workflow_status(self):
        """Get current workflow status from Google Sheets"""
        try:
            # Check if sheets exist and have data
            quiz_questions = self.sheets_manager.get_quiz_questions()
            student_data = self.sheets_manager.get_student_data()
            voice_submissions = self.voice_checker.get_voice_submissions()
            final_results = self.sheets_manager.get_final_results()
            
            status = {
                "quiz_questions_count": len(quiz_questions),
                "student_responses_count": len(student_data),
                "voice_submissions_count": len(voice_submissions),
                "final_results_count": len(final_results),
                "workflow_stage": self._determine_workflow_stage(quiz_questions, student_data, voice_submissions, final_results)
            }
            
            return status
            
        except Exception as e:
            print(f"❌ Error getting workflow status: {e}")
            return {"status": "error", "message": str(e)}
    
    def _determine_workflow_stage(self, quiz_questions, student_data, voice_submissions, final_results):
        """Determine current workflow stage"""
        if not quiz_questions:
            return "quiz_generation"
        elif not student_data:
            return "quiz_submission"
        elif not voice_submissions:
            return "voice_submission"
        elif not final_results:
            return "finalization"
        else:
            return "completed"
