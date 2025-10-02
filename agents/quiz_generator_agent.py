from crewai import Agent, Task
from config import QUIZ_QUESTIONS_COUNT
from google_sheets_manager import GoogleSheetsManager
from llm_manager import llm_manager

class QuizGeneratorAgent:
    def __init__(self):
        self.llm = llm_manager.get_llm()
        self.sheets_manager = GoogleSheetsManager()
    
    def create_agent(self):
        """Create the Quiz Generator Agent"""
        return Agent(
            role='Quiz Generator',
            goal='Generate comprehensive and accurate quiz questions on AI and Data Science topics',
            backstory="""You are an expert educational content creator specializing in AI and Data Science. 
            You have years of experience creating engaging and challenging quiz questions that test 
            both theoretical knowledge and practical understanding. You excel at creating questions 
            that are fair, clear, and appropriately challenging for students at various levels.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def generate_quiz_questions(self, topics):
        """Generate quiz questions based on given topics"""
        try:
            # Create prompt for quiz generation
            prompt = f"""
            Generate {QUIZ_QUESTIONS_COUNT} multiple-choice quiz questions on the following topics: {', '.join(topics)}
            
            Each question should have:
            1. A clear, well-formulated question
            2. Four multiple-choice options (A, B, C, D)
            3. One correct answer
            4. Questions should test both theoretical knowledge and practical understanding
            
            Format each question as:
            Question: [question text]
            A) [option 1]
            B) [option 2]
            C) [option 3]
            D) [option 4]
            Correct Answer: [A/B/C/D]
            
            Make sure questions are:
            - Appropriate for intermediate to advanced level
            - Cover different aspects of AI and Data Science
            - Are clear and unambiguous
            - Have plausible distractors
            """
            
            # Use centralized LLM provider
            from llm_provider import MODEL
            
            response = MODEL.generate_content(prompt)
            print(f"Raw response from OpenAI: {response.text[:200]}...")
            questions_data = self._parse_quiz_response(response.text)
            
            # Store questions in Google Sheets
            self._store_questions_in_sheets(questions_data)
            
            return questions_data
            
        except Exception as e:
            print(f"Error generating quiz questions: {e}")
            return []
    
    def _parse_quiz_response(self, response_text):
        """Parse the generated quiz response into structured data"""
        questions = []
        lines = response_text.split('\n')
        
        current_question = {}
        for line in lines:
            line = line.strip()
            # Handle different question formats
            if line.startswith('Question:') or line.startswith('Question ') or (line.startswith('Question') and ':' in line):
                if current_question and 'correct_answer' in current_question:
                    questions.append(current_question)
                # Extract question text after "Question:" or "Question "
                question_text = line.split(':', 1)[1].strip() if ':' in line else line.replace('Question', '').strip()
                current_question = {'question': question_text}
            elif line.startswith('A)'):
                current_question['option1'] = line.replace('A)', '').strip()
            elif line.startswith('B)'):
                current_question['option2'] = line.replace('B)', '').strip()
            elif line.startswith('C)'):
                current_question['option3'] = line.replace('C)', '').strip()
            elif line.startswith('D)'):
                current_question['option4'] = line.replace('D)', '').strip()
            elif line.startswith('Correct Answer:') or line.startswith('Correct Answer '):
                current_question['correct_answer'] = line.split(':', 1)[1].strip() if ':' in line else line.replace('Correct Answer', '').strip()
        
        # Add the last question
        if current_question and 'correct_answer' in current_question:
            questions.append(current_question)
        
        # Debug: Print what we found
        print(f"Parsed {len(questions)} questions from response")
        for i, q in enumerate(questions):
            print(f"Question {i+1}: {q.get('question', 'No question')[:50]}...")
        
        return questions
    
    def _store_questions_in_sheets(self, questions_data):
        """Store generated questions in Google Sheets"""
        try:
            # Prepare data for Google Sheets
            sheet_data = []
            for question in questions_data:
                row = [
                    question.get('question', ''),
                    question.get('option1', ''),
                    question.get('option2', ''),
                    question.get('option3', ''),
                    question.get('option4', ''),
                    question.get('correct_answer', '')
                ]
                sheet_data.append(row)
            
            # Write to Google Sheets
            self.sheets_manager.write_data(
                'Quiz Questions',
                sheet_data,
                'A2'  # Start from row 2 (after headers)
            )
            
            print(f"Successfully stored {len(questions_data)} questions in Google Sheets")
            
        except Exception as e:
            print(f"Error storing questions in sheets: {e}")
    
    def create_task(self, topics):
        """Create a task for the Quiz Generator Agent"""
        return Task(
            description=f"Generate {QUIZ_QUESTIONS_COUNT} comprehensive quiz questions on topics: {', '.join(topics)}",
            expected_output=f"A list of {QUIZ_QUESTIONS_COUNT} well-structured multiple-choice questions with correct answers",
            agent=self.create_agent()
        )
