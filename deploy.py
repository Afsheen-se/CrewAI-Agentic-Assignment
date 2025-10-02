#!/usr/bin/env python3
"""
Deployment script for AISB Onboarding Process System
This script helps prepare the system for deployment
"""

import os
import sys
import subprocess
import json
from datetime import datetime

def check_requirements():
    """Check if all requirements are installed"""
    print("🔍 Checking requirements...")
    
    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.read().strip().split('\n')
        
        missing_packages = []
        
        for requirement in requirements:
            package_name = requirement.split('==')[0].split('>=')[0].split('<=')[0]
            try:
                __import__(package_name.replace('-', '_'))
            except ImportError:
                missing_packages.append(package_name)
        
        if missing_packages:
            print(f"❌ Missing packages: {', '.join(missing_packages)}")
            print("💡 Run: pip install -r requirements.txt")
            return False
        else:
            print("✅ All requirements satisfied")
            return True
            
    except Exception as e:
        print(f"❌ Error checking requirements: {e}")
        return False

def check_configuration():
    """Check if configuration is properly set up"""
    print("\n🔧 Checking configuration...")
    
    config_checks = {
        "Environment file": os.path.exists('.env'),
        "Credentials file": os.path.exists('credentials.json'),
        "Config module": os.path.exists('config.py')
    }
    
    all_good = True
    
    for check_name, exists in config_checks.items():
        if exists:
            print(f"✅ {check_name}: Found")
        else:
            print(f"❌ {check_name}: Missing")
            all_good = False
    
    if not all_good:
        print("\n💡 Setup instructions:")
        print("1. Copy env_example.txt to .env and configure it")
        print("2. Download Google Sheets credentials as credentials.json")
        print("3. Set up your Google Sheet ID and API keys")
    
    return all_good

def create_deployment_package():
    """Create a deployment package"""
    print("\n📦 Creating deployment package...")
    
    try:
        # Create deployment directory
        deploy_dir = f"deployment_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(deploy_dir, exist_ok=True)
        
        # Files to include in deployment
        files_to_copy = [
            'streamlit_app.py',
            'crewai_workflow.py',
            'google_sheets_manager.py',
            'email_service.py',
            'video_processor.py',
            'config.py',
            'requirements.txt',
            'README.md'
        ]
        
        # Copy files
        for file in files_to_copy:
            if os.path.exists(file):
                subprocess.run(['cp', file, deploy_dir], check=True)
                print(f"✅ Copied {file}")
        
        # Copy agents directory
        if os.path.exists('agents'):
            subprocess.run(['cp', '-r', 'agents', deploy_dir], check=True)
            print("✅ Copied agents directory")
        
        # Create deployment info
        deployment_info = {
            "created_at": datetime.now().isoformat(),
            "version": "1.0.0",
            "files_included": files_to_copy + ['agents/'],
            "deployment_instructions": [
                "1. Install dependencies: pip install -r requirements.txt",
                "2. Configure .env file with your credentials",
                "3. Run: streamlit run streamlit_app.py"
            ]
        }
        
        with open(f"{deploy_dir}/deployment_info.json", 'w') as f:
            json.dump(deployment_info, f, indent=2)
        
        print(f"✅ Deployment package created: {deploy_dir}")
        return deploy_dir
        
    except Exception as e:
        print(f"❌ Error creating deployment package: {e}")
        return None

def generate_streamlit_config():
    """Generate Streamlit configuration for deployment"""
    print("\n⚙️ Generating Streamlit configuration...")
    
    config_content = """[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = false

[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
"""
    
    try:
        with open('streamlit_config.toml', 'w') as f:
            f.write(config_content)
        print("✅ Streamlit configuration created")
        return True
    except Exception as e:
        print(f"❌ Error creating Streamlit config: {e}")
        return False

def create_dockerfile():
    """Create Dockerfile for containerized deployment"""
    print("\n🐳 Creating Dockerfile...")
    
    dockerfile_content = """FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
"""
    
    try:
        with open('Dockerfile', 'w') as f:
            f.write(dockerfile_content)
        print("✅ Dockerfile created")
        return True
    except Exception as e:
        print(f"❌ Error creating Dockerfile: {e}")
        return False

def create_docker_compose():
    """Create docker-compose.yml for easy deployment"""
    print("\n🐳 Creating docker-compose.yml...")
    
    compose_content = """version: '3.8'

services:
  aisb-onboarding:
    build: .
    ports:
      - "8501:8501"
    environment:
      - GOOGLE_SHEETS_CREDENTIALS_FILE=/app/credentials.json
      - GOOGLE_SHEET_ID=${GOOGLE_SHEET_ID}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - EMAIL_USERNAME=${EMAIL_USERNAME}
      - EMAIL_PASSWORD=${EMAIL_PASSWORD}
      - FROM_EMAIL=${FROM_EMAIL}
    volumes:
      - ./credentials.json:/app/credentials.json:ro
    restart: unless-stopped
"""
    
    try:
        with open('docker-compose.yml', 'w') as f:
            f.write(compose_content)
        print("✅ docker-compose.yml created")
        return True
    except Exception as e:
        print(f"❌ Error creating docker-compose.yml: {e}")
        return False

def main():
    """Main deployment function"""
    print("🚀 AISB Onboarding Process - Deployment Preparation")
    print("=" * 60)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Requirements check failed. Please install missing packages.")
        return False
    
    # Check configuration
    if not check_configuration():
        print("\n❌ Configuration check failed. Please set up your configuration.")
        return False
    
    # Generate deployment files
    generate_streamlit_config()
    create_dockerfile()
    create_docker_compose()
    
    # Create deployment package
    deploy_dir = create_deployment_package()
    
    if deploy_dir:
        print(f"\n🎉 Deployment preparation completed!")
        print(f"📦 Deployment package: {deploy_dir}")
        print("\n🚀 Deployment options:")
        print("1. Local deployment: streamlit run streamlit_app.py")
        print("2. Docker deployment: docker-compose up")
        print("3. Streamlit Cloud: Upload to GitHub and connect to Streamlit Cloud")
        print("4. Other cloud platforms: Use the deployment package")
        
        print("\n📋 Next steps:")
        print("1. Configure your .env file with production values")
        print("2. Set up your Google Sheets and API keys")
        print("3. Deploy using your preferred method")
        print("4. Test the deployed application")
        
        return True
    else:
        print("\n❌ Deployment preparation failed")
        return False

if __name__ == "__main__":
    main()
