# 🔧 AISB Onboarding Process - Setup Checklist

## 📋 Complete Setup Guide

### Step 1: Google Sheets Setup

#### 1.1 Create Google Sheet
- [ ] Go to [Google Sheets](https://sheets.google.com)
- [ ] Click "Blank" to create new spreadsheet
- [ ] Name it "AISB Onboarding Process"
- [ ] Copy the Sheet ID from URL (between `/d/` and `/edit`)

#### 1.2 Set up Google Cloud Platform
- [ ] Go to [Google Cloud Console](https://console.cloud.google.com)
- [ ] Create new project: "AISB Onboarding Process"
- [ ] Enable Google Sheets API
- [ ] Create Service Account credentials
- [ ] Download JSON credentials as `credentials.json`

#### 1.3 Share Google Sheet
- [ ] Open your Google Sheet
- [ ] Click "Share" button
- [ ] Add service account email (from credentials.json)
- [ ] Set permission to "Editor"
- [ ] Uncheck "Notify people"

### Step 2: Gemini AI Setup

- [ ] Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
- [ ] Sign in with Google account
- [ ] Click "Create API Key"
- [ ] Copy the generated API key

### Step 3: Email Setup

- [ ] Enable 2-factor authentication on Gmail
- [ ] Go to [Gmail Security](https://myaccount.google.com/security)
- [ ] Click "App passwords"
- [ ] Generate new app password
- [ ] Use this password (not regular Gmail password)

### Step 4: Configuration

- [ ] Copy `env_example.txt` to `.env`
- [ ] Fill in all configuration values:
  - [ ] `GOOGLE_SHEET_ID=your_sheet_id_here`
  - [ ] `GEMINI_API_KEY=your_gemini_key_here`
  - [ ] `EMAIL_USERNAME=your_email@gmail.com`
  - [ ] `EMAIL_PASSWORD=your_app_password_here`
  - [ ] `FROM_EMAIL=your_email@gmail.com`

### Step 5: Test Setup

- [ ] Run: `python setup_guide.py`
- [ ] Run: `python test_system.py`
- [ ] Run: `python run.py`
- [ ] Open: http://localhost:8501

## 🚨 Common Issues & Solutions

### Issue: "credentials.json not found"
**Solution:** Download from Google Cloud Console → Credentials → Service Account → Keys

### Issue: "Permission denied" on Google Sheet
**Solution:** Share sheet with service account email from credentials.json

### Issue: "Invalid API key" for Gemini
**Solution:** Check API key is correct and has proper permissions

### Issue: "Authentication failed" for email
**Solution:** Use App Password, not regular Gmail password

## 📞 Quick Help

### Google Sheets ID Format
```
https://docs.google.com/spreadsheets/d/1ABC123DEF456GHI789JKL/edit#gid=0
                                                      ↑
                                              This is your Sheet ID
```

### Service Account Email Format
```
aisb-onboarding-service@your-project.iam.gserviceaccount.com
```

### .env File Example
```env
GOOGLE_SHEET_ID=1ABC123DEF456GHI789JKL
GEMINI_API_KEY=AIzaSyABC123DEF456GHI789JKL
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_16_character_app_password
```

## ✅ Verification Checklist

- [ ] `credentials.json` exists and is valid JSON
- [ ] Google Sheet is shared with service account
- [ ] `.env` file has all required values
- [ ] All Python packages installed: `pip install -r requirements.txt`
- [ ] System test passes: `python test_system.py`
- [ ] Application starts: `python run.py`
