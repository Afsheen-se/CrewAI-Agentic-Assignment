# Quick smoke test for OpenAI
from llm_provider import MODEL
resp = MODEL.generate_content("Say 'ready' in one word.")
print(resp.text)
