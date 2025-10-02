#!/usr/bin/env python3
"""
Test script for AISB Onboarding Process System
This script tests the basic functionality of the multi-agent system
"""

import os
import sys
from datetime import datetime

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import crewai
        print("✅ CrewAI imported successfully")
    except ImportError as e:
        print(f"❌ CrewAI import failed: {e}")
        return False
    
    try:
        import google.generativeai as genai
        print("✅ Google Generative AI imported successfully")
    except ImportError as e:
        print(f"❌ Google Generative AI import failed: {e}")
        return False
    
    try:
        import streamlit
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import pandas
        print("✅ Pandas imported successfully")
    except ImportError as e:
        print(f"❌ Pandas import failed: {e}")
        return False
    
    return True

def test_config():
    """Test configuration loading"""
    print("\n🔧 Testing configuration...")
    
    try:
        from config import (
            GOOGLE_SHEETS_CREDENTIALS_FILE,
            GOOGLE_SHEET_ID,
            GEMINI_API_KEY,
            EMAIL_USERNAME,
            FROM_EMAIL
        )
        
        config_status = {
            "Google Sheets Credentials": os.path.exists(GOOGLE_SHEETS_CREDENTIALS_FILE) if GOOGLE_SHEETS_CREDENTIALS_FILE else False,
            "Google Sheet ID": bool(GOOGLE_SHEET_ID),
            "Gemini API Key": bool(GEMINI_API_KEY),
            "Email Username": bool(EMAIL_USERNAME),
            "From Email": bool(FROM_EMAIL)
        }
        
        for key, status in config_status.items():
            if status:
                print(f"✅ {key}: Configured")
            else:
                print(f"⚠️ {key}: Not configured")
        
        return config_status
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_agents():
    """Test agent creation"""
    print("\n🤖 Testing agent creation...")
    
    try:
        from agents.quiz_generator_agent import QuizGeneratorAgent
        from agents.quiz_checker_agent import QuizCheckerAgent
        from agents.top10_extractor_agent import Top10ExtractorAgent
        from agents.video_checker_agent import VideoCheckerAgent
        from agents.finalizer_agent import FinalizerAgent
        
        # Test agent creation
        quiz_gen = QuizGeneratorAgent()
        quiz_check = QuizCheckerAgent()
        top10_ext = Top10ExtractorAgent()
        video_check = VideoCheckerAgent()
        finalizer = FinalizerAgent()
        
        print("✅ All agents created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Agent creation failed: {e}")
        return False

def test_workflow():
    """Test workflow creation"""
    print("\n🔄 Testing workflow creation...")
    
    try:
        from crewai_workflow import AISBOnboardingWorkflow
        
        workflow = AISBOnboardingWorkflow()
        print("✅ Workflow created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Workflow creation failed: {e}")
        return False

def test_google_sheets():
    """Test Google Sheets connection"""
    print("\n📊 Testing Google Sheets connection...")
    
    try:
        from google_sheets_manager import GoogleSheetsManager
        
        sheets_manager = GoogleSheetsManager()
        print("✅ Google Sheets manager created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Google Sheets connection failed: {e}")
        print("💡 Make sure credentials.json is properly configured")
        return False

def test_email_service():
    """Test email service"""
    print("\n📧 Testing email service...")
    
    try:
        from email_service import EmailService
        
        email_service = EmailService()
        print("✅ Email service created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Email service creation failed: {e}")
        return False

def test_video_processor():
    """Test video processor"""
    print("\n🎥 Testing video processor...")
    
    try:
        from video_processor import VideoProcessor
        
        video_processor = VideoProcessor()
        print("✅ Video processor created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Video processor creation failed: {e}")
        return False

def run_basic_workflow_test():
    """Run a basic workflow test"""
    print("\n🚀 Running basic workflow test...")
    
    try:
        from crewai_workflow import AISBOnboardingWorkflow
        
        workflow = AISBOnboardingWorkflow()
        
        # Test quiz generation with sample topics
        topics = ["Artificial Intelligence", "Machine Learning", "Data Science"]
        
        print("📝 Testing quiz generation...")
        result = workflow.run_quiz_generation_only(topics)
        
        if result["status"] == "completed":
            print(f"✅ Quiz generation successful: {len(result['quiz_questions'])} questions")
            return True
        else:
            print(f"❌ Quiz generation failed: {result.get('message', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Workflow test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🎓 AISB Onboarding Process - System Test")
    print("=" * 50)
    
    test_results = []
    
    # Run all tests
    test_results.append(("Imports", test_imports()))
    test_results.append(("Configuration", test_config()))
    test_results.append(("Agents", test_agents()))
    test_results.append(("Workflow", test_workflow()))
    test_results.append(("Google Sheets", test_google_sheets()))
    test_results.append(("Email Service", test_email_service()))
    test_results.append(("Video Processor", test_video_processor()))
    test_results.append(("Basic Workflow", run_basic_workflow_test()))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary")
    print("=" * 50)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        if result:
            print(f"✅ {test_name}: PASSED")
            passed += 1
        else:
            print(f"❌ {test_name}: FAILED")
    
    print(f"\n🎯 Overall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        print("\n🚀 To start the application, run:")
        print("   streamlit run streamlit_app.py")
    else:
        print("⚠️ Some tests failed. Please check the configuration and dependencies.")
        print("\n💡 Common issues:")
        print("   - Missing dependencies: pip install -r requirements.txt")
        print("   - Configuration: Check .env file and credentials")
        print("   - Google Sheets: Ensure credentials.json is properly configured")

if __name__ == "__main__":
    main()
