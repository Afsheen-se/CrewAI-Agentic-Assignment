#!/usr/bin/env python3
"""
Setup Guide for AISB Onboarding Process System
This script helps you set up Google Sheets and other configurations
"""

import os
import json
import webbrowser
from datetime import datetime

def print_header():
    """Print setup header"""
    print("🎓 AISB Onboarding Process - Setup Guide")
    print("=" * 50)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

def check_existing_setup():
    """Check if setup already exists"""
    print("🔍 Checking existing setup...")
    
    setup_status = {
        "credentials.json": os.path.exists("credentials.json"),
        ".env": os.path.exists(".env"),
        "config.py": os.path.exists("config.py")
    }
    
    for item, exists in setup_status.items():
        if exists:
            print(f"✅ {item}: Found")
        else:
            print(f"❌ {item}: Missing")
    
    return setup_status

def guide_google_sheets_setup():
    """Guide user through Google Sheets setup"""
    print("\n📊 Google Sheets Setup Guide")
    print("=" * 30)
    
    print("1. Create a new Google Sheet:")
    print("   → Go to: https://sheets.google.com")
    print("   → Click 'Blank' to create new spreadsheet")
    print("   → Name it: 'AISB Onboarding Process'")
    
    print("\n2. Get your Sheet ID:")
    print("   → Look at the URL in your browser")
    print("   → Copy the ID between '/d/' and '/edit'")
    print("   → Example: https://docs.google.com/spreadsheets/d/1ABC123DEF456GHI789JKL/edit")
    print("   → Sheet ID: 1ABC123DEF456GHI789JKL")
    
    sheet_id = input("\n📝 Enter your Google Sheet ID: ").strip()
    
    print("\n3. Set up Google Cloud Platform:")
    print("   → Go to: https://console.cloud.google.com")
    print("   → Create a new project")
    print("   → Enable Google Sheets API")
    print("   → Create Service Account credentials")
    print("   → Download JSON credentials file")
    
    print("\n4. Share your Google Sheet:")
    print("   → Open your Google Sheet")
    print("   → Click 'Share' button")
    print("   → Add the service account email (from credentials.json)")
    print("   → Set permission to 'Editor'")
    
    return sheet_id

def guide_gemini_setup():
    """Guide user through Gemini API setup"""
    print("\n🤖 Gemini API Setup Guide")
    print("=" * 25)
    
    print("1. Get Gemini API Key:")
    print("   → Go to: https://makersuite.google.com/app/apikey")
    print("   → Sign in with your Google account")
    print("   → Click 'Create API Key'")
    print("   → Copy the generated API key")
    
    api_key = input("\n📝 Enter your Gemini API Key: ").strip()
    return api_key

def guide_email_setup():
    """Guide user through email setup"""
    print("\n📧 Email Setup Guide")
    print("=" * 20)
    
    print("1. Gmail App Password Setup:")
    print("   → Enable 2-factor authentication on Gmail")
    print("   → Go to: https://myaccount.google.com/security")
    print("   → Click 'App passwords'")
    print("   → Generate a new app password")
    print("   → Use this password (not your regular Gmail password)")
    
    email = input("\n📝 Enter your Gmail address: ").strip()
    password = input("📝 Enter your Gmail App Password: ").strip()
    
    return email, password

def create_env_file(sheet_id, gemini_key, email, password):
    """Create .env file with configuration"""
    print("\n📝 Creating .env file...")
    
    env_content = f"""# Google Sheets Configuration
GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
GOOGLE_SHEET_ID={sheet_id}

# Gemini API Configuration
GEMINI_API_KEY={gemini_key}

# Email Configuration
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_USERNAME={email}
EMAIL_PASSWORD={password}
FROM_EMAIL={email}
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def verify_setup():
    """Verify the setup"""
    print("\n🔍 Verifying setup...")
    
    # Check if credentials.json exists
    if not os.path.exists("credentials.json"):
        print("❌ credentials.json not found")
        print("💡 Please download it from Google Cloud Console")
        return False
    
    # Check if .env exists
    if not os.path.exists(".env"):
        print("❌ .env file not found")
        return False
    
    # Check credentials.json format
    try:
        with open("credentials.json", 'r') as f:
            creds = json.load(f)
        
        required_fields = ["type", "project_id", "private_key", "client_email"]
        for field in required_fields:
            if field not in creds:
                print(f"❌ credentials.json missing field: {field}")
                return False
        
        print("✅ credentials.json format is correct")
        
    except json.JSONDecodeError:
        print("❌ credentials.json is not valid JSON")
        return False
    except Exception as e:
        print(f"❌ Error reading credentials.json: {e}")
        return False
    
    print("✅ Setup verification completed")
    return True

def open_helpful_links():
    """Open helpful links in browser"""
    print("\n🌐 Opening helpful links...")
    
    links = {
        "Google Sheets": "https://sheets.google.com",
        "Google Cloud Console": "https://console.cloud.google.com",
        "Gemini API": "https://makersuite.google.com/app/apikey",
        "Gmail Security": "https://myaccount.google.com/security"
    }
    
    for name, url in links.items():
        try:
            webbrowser.open(url)
            print(f"✅ Opened {name}")
        except Exception as e:
            print(f"❌ Could not open {name}: {e}")

def main():
    """Main setup function"""
    print_header()
    
    # Check existing setup
    setup_status = check_existing_setup()
    
    if all(setup_status.values()):
        print("\n🎉 Setup already complete!")
        response = input("Do you want to reconfigure? (y/N): ")
        if response.lower() != 'y':
            print("👋 Setup cancelled")
            return
    
    print("\n🚀 Let's set up your AISB Onboarding Process system!")
    print("This will guide you through the complete setup process.")
    
    # Get user input
    sheet_id = guide_google_sheets_setup()
    gemini_key = guide_gemini_setup()
    email, password = guide_email_setup()
    
    # Create .env file
    if create_env_file(sheet_id, gemini_key, email, password):
        print("\n✅ Configuration saved!")
    else:
        print("\n❌ Failed to save configuration")
        return
    
    # Verify setup
    if verify_setup():
        print("\n🎉 Setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Make sure credentials.json is in your project folder")
        print("2. Share your Google Sheet with the service account email")
        print("3. Run: python run.py")
        print("4. Open: http://localhost:8501")
    else:
        print("\n⚠️ Setup incomplete. Please check the issues above.")
    
    # Offer to open helpful links
    response = input("\n🌐 Open helpful setup links in browser? (y/N): ")
    if response.lower() == 'y':
        open_helpful_links()

if __name__ == "__main__":
    main()
