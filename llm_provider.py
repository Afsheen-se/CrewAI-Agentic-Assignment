import os
from dotenv import load_dotenv
import openai

load_dotenv()
API_KEY = os.environ.get("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY in .env")

# Configure OpenAI
openai.api_key = API_KEY

# OpenAI model (use GPT-4 or GPT-3.5-turbo)
MODEL_ID = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")

class OpenAIModel:
    def __init__(self, model_id):
        self.model_id = model_id
        self.client = openai.OpenAI(api_key=API_KEY)
    
    def generate_content(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
            return type('Response', (), {'text': response.choices[0].message.content})()
        except Exception as e:
            print(f"Error with OpenAI API: {e}")
            raise

MODEL = OpenAIModel(MODEL_ID)
