import streamlit as st
import pandas as pd
import json
from datetime import datetime
from crewai_workflow import AISBOnboardingWorkflow
from google_sheets_manager import GoogleSheetsManager
from email_service import EmailService
import time

def calculate_student_score(responses):
    """Calculate student score by comparing responses with quiz questions"""
    try:
        # Get quiz questions from Google Sheets
        sheets_manager = get_sheets_manager()
        questions = sheets_manager.get_quiz_questions()
        
        if not questions or not responses:
            return 0
        
        if len(responses) != len(questions):
            return 0
        
        correct_count = 0
        for i, question in enumerate(questions):
            if i < len(responses):
                student_answer = responses[i].upper().strip()
                correct_answer = question['correct_answer'].upper().strip()
                
                if student_answer == correct_answer:
                    correct_count += 1
        
        return correct_count
        
    except Exception as e:
        print(f"Error calculating score: {e}")
        return 0

# Page configuration
st.set_page_config(
    page_title="AISB Onboarding Process",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize workflow
@st.cache_resource
def get_workflow():
    return AISBOnboardingWorkflow()

@st.cache_resource
def get_sheets_manager():
    return GoogleSheetsManager()

@st.cache_resource
def get_email_service():
    return EmailService()

def main():
    st.title("🎓 AISB Onboarding Process Management System")
    
    st.markdown("---")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Select Page",
        [
            "🏠 Dashboard",
            "📝 Quiz Management",
            "📊 Student Management", 
            "🎵 Voice Submissions",
            "🏆 Final Results",
            "⚙️ Settings"
        ]
    )
    
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "📝 Quiz Management":
        show_quiz_management()
    elif page == "📊 Student Management":
        show_student_management()
    elif page == "🎵 Voice Submissions":
        show_voice_management()
    elif page == "🏆 Final Results":
        show_final_results()
    elif page == "⚙️ Settings":
        show_settings()

def show_dashboard():
    st.header("📊 Dashboard")
    
    workflow = get_workflow()
    sheets_manager = get_sheets_manager()
    
    # Get workflow status
    try:
        status = workflow.get_workflow_status()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Quiz Questions", status.get("quiz_questions_count", 0))
        
        with col2:
            st.metric("Student Responses", status.get("student_responses_count", 0))
        
        with col3:
            st.metric("Voice Submissions", status.get("voice_submissions_count", 0))
        
        with col4:
            st.metric("Final Results", status.get("final_results_count", 0))
        
        # Workflow stage
        stage = status.get("workflow_stage", "unknown")
        st.info(f"Current Workflow Stage: {stage.replace('_', ' ').title()}")
        
        # Quick actions
        st.subheader("🚀 Quick Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Refresh Status", type="primary"):
                st.rerun()
        
            
    except Exception as e:
        st.error(f"Error loading dashboard: {e}")

def show_quiz_management():
    st.header("📝 Quiz Management")
    
    workflow = get_workflow()
    
    # Quiz Generation
    st.subheader("Generate Quiz Questions")
    
    topics_input = st.text_area(
        "Enter topics (one per line):",
        value="Artificial Intelligence\nMachine Learning\nData Science\nPython Programming\nStatistics",
        height=100
    )
    
    if st.button("Generate Quiz Questions", type="primary"):
        with st.spinner("Generating quiz questions..."):
            topics = [topic.strip() for topic in topics_input.split('\n') if topic.strip()]
            result = workflow.run_quiz_generation_only(topics)
            
            if result["status"] == "completed":
                st.success(f"✅ Generated {len(result['quiz_questions'])} quiz questions!")
                st.session_state.quiz_generated = True
            else:
                st.error(f"❌ Error: {result.get('message', 'Unknown error')}")
    
    # Display quiz questions
    if st.session_state.get("quiz_generated", False):
        st.subheader("📋 Generated Quiz Questions")
        
        try:
            sheets_manager = get_sheets_manager()
            questions = sheets_manager.get_quiz_questions()
            
            if questions:
                for i, question in enumerate(questions, 1):
                    with st.expander(f"Question {i}: {question['question'][:50]}..."):
                        st.write(f"**Question:** {question['question']}")
                        st.write(f"**A)** {question['option1']}")
                        st.write(f"**B)** {question['option2']}")
                        st.write(f"**C)** {question['option3']}")
                        st.write(f"**D)** {question['option4']}")
                        st.write(f"**Correct Answer:** {question['correct_answer']}")
            else:
                st.info("No quiz questions found. Generate some first!")
                
        except Exception as e:
            st.error(f"Error loading quiz questions: {e}")

def show_student_management():
    st.header("📊 Student Management")
    
    workflow = get_workflow()
    sheets_manager = get_sheets_manager()
    
    # Clear all records button
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("Add Student")
    
    with col2:
        if st.button("Clear All Records", type="secondary"):
            with st.spinner("Clearing all student records..."):
                try:
                    sheets_manager.clear_sheet('Student Data')
                    st.success("✅ All student records cleared!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error clearing records: {e}")
    
    with st.form("student_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            student_name = st.text_input("Student Name", placeholder="Enter student name")
            student_email = st.text_input("Student Email", placeholder="Enter student email")
        
        with col2:
            st.info("💡 **Note:** Quiz responses will be automatically calculated when students attempt the quiz. You can add students without responses for now.")
            student_responses = st.text_input("Quiz Responses (Optional)", placeholder="Leave empty for automatic scoring", 
                                           help="Leave empty to let students attempt quiz and get automatic scoring")
        
        submitted = st.form_submit_button("Add Student", type="primary")
        
        if submitted:
            if student_name and student_email:
                if student_responses:
                    # Student has responses - process them
                    responses = [r.strip() for r in student_responses.split(',')]
                    calculated_score = calculate_student_score(responses)
                    
                    student_data = {
                        "name": student_name,
                        "email": student_email,
                        "responses": responses,
                        "marks": calculated_score
                    }
                    
                    with st.spinner("Adding student with responses..."):
                        result = workflow.run_quiz_checking_only([student_data])
                        
                        if result["status"] == "completed":
                            st.success(f"✅ Added student: {student_name} - Score: {calculated_score}/10")
                        else:
                            st.error(f"❌ Error: {result.get('message', 'Unknown error')}")
                else:
                    # Student without responses - add to database for quiz invitation
                    with st.spinner("Adding student for quiz invitation..."):
                        try:
                            # Add student to Google Sheets without responses
                            row_data = [student_name, student_email, 0, "", "PENDING"]
                            sheets_manager.append_data('Student Data', [row_data])
                            st.success(f"✅ Added student: {student_name} - Will receive quiz invitation")
                        except Exception as e:
                            st.error(f"❌ Error adding student: {e}")
            else:
                st.error("Please fill in both name and email")
    
    
    
    # Quiz attempt section
    st.subheader("Quiz Attempt")
    
    st.info("""
    **How it works:**
    1. Add students without responses (they'll be marked as PENDING)
    2. Students receive quiz invitation emails
    3. Students attempt the quiz and submit responses
    4. System automatically calculates scores and updates status
    
    **Note**: If emails fail to send, you can manually share the quiz questions with students.
    """)
    
    if st.button("Send Quiz Invitations to Pending Students", type="primary"):
        with st.spinner("Sending quiz invitations..."):
            try:
                # Get all pending students
                student_data = sheets_manager.get_student_data()
                pending_students = [s for s in student_data if s.get('status') == 'PENDING']
                
                if pending_students:
                    # Send quiz invitations
                    email_service = get_email_service()
                    sent_count = 0
                    
                    for student in pending_students:
                        try:
                            success = email_service.send_quiz_invitation(
                                student['email'],
                                student['name'],
                                "https://your-quiz-link.com"  # Replace with actual quiz link
                            )
                            if success:
                                sent_count += 1
                                st.write(f"✅ Sent to {student['name']} ({student['email']})")
                            else:
                                st.write(f"❌ Failed to send to {student['name']} ({student['email']})")
                        except Exception as e:
                            st.write(f"❌ Error sending to {student['name']}: {str(e)}")
                    
                    if sent_count > 0:
                        st.success(f"✅ Successfully sent quiz invitations to {sent_count} students!")
                    else:
                        st.error("❌ Failed to send any quiz invitations. Please check your email configuration.")
                        st.info("💡 **Email Issue**: Check your Gmail settings, app password, and network connection.")
                else:
                    st.info("No pending students found.")
                    
            except Exception as e:
                st.error(f"❌ Error sending invitations: {e}")
    
    # Display student data
    st.subheader("Student Data")
    
    try:
        student_data = sheets_manager.get_student_data()
        
        if student_data:
            df = pd.DataFrame(student_data)
            st.dataframe(df, use_container_width=True)
            
            # Send video invitations to passed students
            if st.button("Send Voice Invitations", type="primary"):
                with st.spinner("Sending invitations..."):
                    result = workflow.run_top10_extraction_only()
                    
                    if result["status"] == "completed":
                        st.success(f"✅ Sent invitations to {len(result['top_students'])} students!")
                    else:
                        st.error(f"❌ Error: {result.get('message', 'Unknown error')}")
        else:
            st.info("No student data found. Add some students first!")
            
    except Exception as e:
        st.error(f"Error loading student data: {e}")

def show_voice_management():
    st.header("🎵 Voice Submissions")
    
    workflow = get_workflow()
    sheets_manager = get_sheets_manager()
    
    # Voice submission input
    st.subheader("Add Voice Submissions")
    
    with st.form("video_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            student_name = st.text_input("Student Name", placeholder="Enter student name")
        
        with col2:
            voice_link = st.text_input("Voice Recording Link", placeholder="https://drive.google.com/file/d/... (1-minute audio introduction)")
        
        submitted = st.form_submit_button("Add Voice Recording", type="primary")
        
        if submitted:
            if student_name and voice_link:
                with st.spinner("Processing voice recording..."):
                    result = workflow.run_video_processing_only([{
                        "student_name": student_name,
                        "voice_link": voice_link
                    }])
                    
                    if result["status"] == "completed":
                        st.success(f"✅ Voice recording processed for {student_name}!")
                    else:
                        st.error(f"❌ Error: {result.get('message', 'Unknown error')}")
            else:
                st.error("Please fill in both name and voice recording link")
    
    # Display voice submissions
    st.subheader("Voice Submissions")
    
    try:
        voice_data = sheets_manager.read_data('Voice Submissions', 'A:E')
        
        if len(voice_data) > 1:  # More than just headers
            df = pd.DataFrame(voice_data[1:], columns=voice_data[0])
            st.dataframe(df, use_container_width=True)
            
            # Finalization
            if st.button("Finalize Selection", type="primary"):
                with st.spinner("Finalizing selection..."):
                    result = workflow.run_finalization_only()
                    
                    if result["status"] == "completed":
                        st.success(f"✅ Finalized selection with {len(result['final_selection'])} students!")
                    else:
                        st.error(f"❌ Error: {result.get('message', 'Unknown error')}")
        else:
            st.info("No voice submissions found. Process some voice recordings first!")
            
    except Exception as e:
        st.error(f"Error loading voice data: {e}")

def show_final_results():
    st.header("🏆 Final Results")
    
    sheets_manager = get_sheets_manager()
    
    try:
        final_results = sheets_manager.get_final_results()
        
        if final_results:
            df = pd.DataFrame(final_results)
            
            # Summary statistics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Students", len(df))
            
            with col2:
                selected_count = len(df[df['status'] == 'Selected'])
                st.metric("Selected Students", selected_count)
            
            with col3:
                avg_score = df['total_score'].mean()
                st.metric("Average Score", f"{avg_score:.1f}")
            
            # Results table
            st.subheader("Results")
            st.dataframe(df, use_container_width=True)
            
            # Top 5 students
            if selected_count > 0:
                st.subheader("Selected Students")
                top_5 = df[df['status'] == 'Selected'].head(5)
                st.dataframe(top_5, use_container_width=True)
            
            # Download results
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv,
                file_name=f"aisb_final_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.info("No final results found. Complete the workflow first!")
            
    except Exception as e:
        st.error(f"Error loading final results: {e}")

def show_settings():
    st.header("⚙️ Settings")
    
    st.subheader("🔧 Configuration")
    
    # Google Sheets settings
    st.write("**Google Sheets Configuration:**")
    st.code("""
    GOOGLE_SHEET_ID=your_google_sheet_id_here
    GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
    """)
    
    # Gemini API settings
    st.write("**Gemini API Configuration:**")
    st.code("""
    GEMINI_API_KEY=your_gemini_api_key_here
    """)
    
    # Email settings
    st.write("**Email Configuration:**")
    st.code("""
    EMAIL_USERNAME=your_email@gmail.com
    EMAIL_PASSWORD=your_app_password_here
    FROM_EMAIL=your_email@gmail.com
    """)
    
    st.subheader("📋 Setup Instructions")
    
    with st.expander("🔧 How to Setup"):
        st.markdown("""
        1. **Google Sheets Setup:**
           - Create a new Google Sheet
           - Enable Google Sheets API
           - Download credentials.json
           - Set GOOGLE_SHEET_ID in .env file
        
        2. **Gemini API Setup:**
           - Get API key from Google AI Studio
           - Set GEMINI_API_KEY in .env file
        
        3. **Email Setup:**
           - Use Gmail with App Password
           - Set email credentials in .env file
        
        4. **Install Dependencies:**
           - Run: pip install -r requirements.txt
        
        5. **Run Application:**
           - Run: streamlit run streamlit_app.py
        """)
    
    # System status
    st.subheader("🔍 System Status")
    
    try:
        sheets_manager = get_sheets_manager()
        st.success("✅ Google Sheets connection: OK")
    except Exception as e:
        st.error(f"❌ Google Sheets connection: {e}")
    
    try:
        from config import GEMINI_API_KEY
        if GEMINI_API_KEY:
            st.success("✅ Gemini API key: Configured")
        else:
            st.warning("⚠️ Gemini API key: Not configured")
    except:
        st.error("❌ Gemini API key: Error")
    
    try:
        from config import EMAIL_USERNAME
        if EMAIL_USERNAME:
            st.success("✅ Email configuration: OK")
        else:
            st.warning("⚠️ Email configuration: Not configured")
    except:
        st.error("❌ Email configuration: Error")

def show_all_data():
    st.subheader("📊 All Data Overview")
    
    sheets_manager = get_sheets_manager()
    
    try:
        # Quiz questions
        st.write("**Quiz Questions:**")
        questions = sheets_manager.get_quiz_questions()
        if questions:
            st.write(f"Count: {len(questions)}")
        else:
            st.write("No quiz questions found")
        
        # Student data
        st.write("**Student Data:**")
        students = sheets_manager.get_student_data()
        if students:
            st.write(f"Count: {len(students)}")
        else:
            st.write("No student data found")
        
        # Voice submissions
        st.write("**Voice Submissions:**")
        voices = sheets_manager.read_data('Voice Submissions', 'A:E')
        if len(voices) > 1:
            st.write(f"Count: {len(voices) - 1}")
        else:
            st.write("No voice submissions found")
        
        # Final results
        st.write("**Final Results:**")
        results = sheets_manager.get_final_results()
        if results:
            st.write(f"Count: {len(results)}")
        else:
            st.write("No final results found")
            
    except Exception as e:
        st.error(f"Error loading data overview: {e}")

if __name__ == "__main__":
    main()
