from crewai import LLM
from llm_provider import MODEL_ID, API_KEY

class LLMManager:
    def __init__(self):
        self.llm = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize OpenAI model using CrewAI LLM"""
        try:
            # Use CrewAI LLM format with OpenAI provider
            self.llm = LLM(
                model=f"openai/{MODEL_ID}",   # e.g., openai/gpt-3.5-turbo
                api_key=API_KEY,
                temperature=0.2
            )
            
            print(f"✅ Successfully initialized OpenAI {MODEL_ID} with CrewAI LLM")
            
        except Exception as e:
            print(f"❌ Error initializing OpenAI: {e}")
            print("💡 Make sure your OPENAI_API_KEY is correct and has access to OpenAI models")
            print("💡 Try checking your API key at: https://platform.openai.com/api-keys")
            raise
    
    def get_llm(self):
        """Get the initialized LLM"""
        return self.llm
    
    def generate_content(self, prompt):
        """Generate content using the model"""
        try:
            from llm_provider import MODEL
            response = MODEL.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"❌ Error generating content: {e}")
            return None

# Global LLM instance
llm_manager = LLMManager()
