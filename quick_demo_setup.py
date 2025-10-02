"""
Quick Demo Setup Script
Run this to populate your app with demo data for testing
"""

from google_sheets_manager import GoogleSheetsManager
import time

def setup_demo_data():
    """Add demo data to Google Sheets for testing"""
    
    print("🚀 Setting up demo data...")
    sheets_manager = GoogleSheetsManager()
    
    # 1. Add sample quiz questions
    print("📝 Adding sample quiz questions...")
    
    # Clear existing data
    sheets_manager.clear_sheet('Quiz Questions')
    
    # Add headers
    quiz_headers = ['Question', 'Option1', 'Option2', 'Option3', 'Option4', 'Correct Answer']
    sheets_manager.append_data('Quiz Questions', [quiz_headers])
    
    # Sample questions
    questions = [
        [
            "What is the primary goal of supervised learning?",
            "To find hidden patterns in data",
            "To learn from labeled training data", 
            "To reduce dimensionality",
            "To cluster similar data points",
            "B"
        ],
        [
            "Which algorithm is commonly used for classification tasks?",
            "K-means clustering",
            "Linear regression",
            "Random Forest",
            "PCA",
            "C"
        ],
        [
            "What does overfitting mean in machine learning?",
            "Model performs well on training but poorly on test data",
            "Model has too few parameters",
            "Model trains too quickly", 
            "Model uses too much memory",
            "A"
        ],
        [
            "Which metric is used to evaluate regression models?",
            "Accuracy",
            "Precision", 
            "Recall",
            "Mean Squared Error",
            "D"
        ],
        [
            "What is the purpose of cross-validation?",
            "To increase model complexity",
            "To assess model performance",
            "To reduce training time",
            "To visualize data",
            "B"
        ],
        [
            "Which is a popular deep learning framework?",
            "Scikit-learn",
            "TensorFlow",
            "Pandas",
            "NumPy", 
            "B"
        ],
        [
            "What is gradient descent used for?",
            "Data preprocessing",
            "Feature selection",
            "Model optimization",
            "Data visualization",
            "C"
        ],
        [
            "Which technique is used to prevent overfitting?",
            "Increasing model complexity",
            "Regularization",
            "Using more features",
            "Reducing training data",
            "B"
        ],
        [
            "What is the main advantage of ensemble methods?",
            "Faster training",
            "Less memory usage", 
            "Improved accuracy",
            "Simpler interpretation",
            "C"
        ],
        [
            "Which activation function is commonly used in hidden layers?",
            "Sigmoid",
            "ReLU",
            "Linear",
            "Step function",
            "B"
        ]
    ]
    
    for question in questions:
        sheets_manager.append_data('Quiz Questions', [question])
    
    print(f"✅ Added {len(questions)} quiz questions")
    
    # 2. Add sample students
    print("👥 Adding sample students...")
    
    # Clear existing data
    sheets_manager.clear_sheet('Student Data')
    
    # Add headers
    student_headers = ['Name', 'Email', 'Quiz Score', 'Video Score', 'Status']
    sheets_manager.append_data('Student Data', [student_headers])
    
    # Sample students (some pass, some fail)
    students = [
        ['John Smith', 'john.smith@demo.com', 8, 0, 'PASSED'],
        ['Sarah Johnson', 'sarah.johnson@demo.com', 9, 0, 'PASSED'], 
        ['Mike Brown', 'mike.brown@demo.com', 5, 0, 'FAILED'],
        ['Lisa Davis', 'lisa.davis@demo.com', 7, 0, 'PASSED'],
        ['David Wilson', 'david.wilson@demo.com', 4, 0, 'FAILED']
    ]
    
    for student in students:
        sheets_manager.append_data('Student Data', [student])
    
    print(f"✅ Added {len(students)} sample students")
    
    # 3. Add sample voice submissions
    print("🎵 Adding sample voice submissions...")
    
    # Clear existing data
    sheets_manager.clear_sheet('Voice Submissions')
    
    # Add headers  
    voice_headers = ['Student Name', 'Voice Link', 'Transcript', 'Score', 'Analysis']
    sheets_manager.append_data('Voice Submissions', [voice_headers])
    
    # Sample voice submissions (only for passed students)
    # These are demo links that will work with the voice processor
    voices = [
        [
            'John Smith',
            'https://drive.google.com/file/d/1ABC123DEF456/view',
            'Hello, my name is John Smith. I\'m passionate about artificial intelligence and machine learning. I have 3 years of experience working with Python and data analysis...',
            8,
            'Strong technical background, clear communication, good passion for AI field'
        ],
        [
            'Sarah Johnson', 
            'https://drive.google.com/file/d/1GHI789JKL012/view',
            'Hi everyone, I\'m Sarah Johnson. I\'ve been working in data science for 2 years and I absolutely love solving complex problems using machine learning algorithms...',
            9,
            'Excellent problem-solving skills, great experience, very articulate presentation'
        ],
        [
            'Lisa Davis',
            'https://drive.google.com/file/d/1MNO345PQR678/view', 
            'Hello, I\'m Lisa Davis. I recently graduated with a degree in computer science and I\'m excited to dive deeper into the world of artificial intelligence...',
            7,
            'Good educational background, enthusiasm for learning, clear career goals'
        ]
    ]
    
    for voice in voices:
        sheets_manager.append_data('Voice Submissions', [voice])
    
    print(f"✅ Added {len(voices)} voice submissions")
    
    # 4. Add final results
    print("🏆 Adding final results...")
    
    # Clear existing data
    sheets_manager.clear_sheet('Final Results')
    
    # Add headers
    final_headers = ['Name', 'Email', 'Quiz Score', 'Voice Score', 'Total Score', 'Status']
    sheets_manager.append_data('Final Results', [final_headers])
    
    # Final results (combined quiz + voice scores)
    final_results = [
        ['Sarah Johnson', 'sarah.johnson@demo.com', 9, 9, 9.0, 'Selected'],
        ['John Smith', 'john.smith@demo.com', 8, 8, 8.0, 'Selected'], 
        ['Lisa Davis', 'lisa.davis@demo.com', 7, 7, 7.0, 'Selected'],
        ['Mike Brown', 'mike.brown@demo.com', 5, 0, 2.5, 'Not Selected'],
        ['David Wilson', 'david.wilson@demo.com', 4, 0, 2.0, 'Not Selected']
    ]
    
    for result in final_results:
        sheets_manager.append_data('Final Results', [result])
    
    print(f"✅ Added {len(final_results)} final results")
    
    print("\n🎉 Demo data setup complete!")
    print("\n📋 What was added:")
    print(f"   • {len(questions)} Quiz Questions")
    print(f"   • {len(students)} Students (3 passed, 2 failed)")
    print(f"   • {len(voices)} Voice Submissions")
    print(f"   • {len(final_results)} Final Results")
    
    print("\n🚀 Your app is now ready for demo!")
    print("   Run: streamlit run streamlit_app.py")

if __name__ == "__main__":
    setup_demo_data()
