#!/usr/bin/env python3
"""
Startup script for AISB Onboarding Process System
This script provides an easy way to start the application
"""

import os
import sys
import subprocess
import time
from datetime import datetime

def check_system():
    """Check if the system is ready to run"""
    print("🔍 Checking system readiness...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        return False
    
    # Check if required files exist
    required_files = [
        'streamlit_app.py',
        'crewai_workflow.py',
        'config.py',
        'requirements.txt'
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Required file missing: {file}")
            return False
    
    # Check if agents directory exists
    if not os.path.exists('agents'):
        print("❌ Agents directory missing")
        return False
    
    print("✅ System check passed")
    return True

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True, capture_output=True, text=True)
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def check_configuration():
    """Check if configuration is set up"""
    print("🔧 Checking configuration...")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️ .env file not found")
        print("💡 Copy env_example.txt to .env and configure it")
        return False
    
    # Check if credentials.json exists
    if not os.path.exists('credentials.json'):
        print("⚠️ credentials.json not found")
        print("💡 Download Google Sheets credentials and save as credentials.json")
        return False
    
    print("✅ Configuration files found")
    return True

def start_streamlit():
    """Start the Streamlit application"""
    print("🚀 Starting Streamlit application...")
    
    try:
        # Set environment variables for Streamlit
        env = os.environ.copy()
        env['STREAMLIT_SERVER_HEADLESS'] = 'true'
        env['STREAMLIT_SERVER_PORT'] = '8501'
        
        # Start Streamlit
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 'streamlit_app.py',
            '--server.port=8501',
            '--server.address=0.0.0.0'
        ], env=env)
        
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")

def run_tests():
    """Run system tests"""
    print("🧪 Running system tests...")
    
    try:
        subprocess.run([sys.executable, 'test_system.py'], check=True)
        print("✅ Tests passed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Tests failed")
        return False

def main():
    """Main function"""
    print("🎓 AISB Onboarding Process - Startup")
    print("=" * 50)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check system
    if not check_system():
        print("\n❌ System check failed. Please fix the issues above.")
        return False
    
    # Install requirements if needed
    try:
        import streamlit
        import crewai
        import google.generativeai
        print("✅ All required packages are installed")
    except ImportError:
        print("📦 Installing required packages...")
        if not install_requirements():
            print("❌ Failed to install requirements")
            return False
    
    # Check configuration
    if not check_configuration():
        print("\n⚠️ Configuration not complete. Please set up your configuration files.")
        print("📋 Required setup:")
        print("1. Copy env_example.txt to .env")
        print("2. Configure your API keys and credentials in .env")
        print("3. Download Google Sheets credentials as credentials.json")
        print("4. Set up your Google Sheet ID")
        
        response = input("\nDo you want to continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("👋 Setup cancelled. Please configure the system first.")
            return False
    
    # Run tests
    print("\n🧪 Running system tests...")
    if not run_tests():
        print("⚠️ Some tests failed, but continuing...")
    
    # Start application
    print("\n🚀 Starting application...")
    print("🌐 Application will be available at: http://localhost:8501")
    print("⏹️ Press Ctrl+C to stop the application")
    print()
    
    try:
        start_streamlit()
    except KeyboardInterrupt:
        print("\n👋 Application stopped")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
