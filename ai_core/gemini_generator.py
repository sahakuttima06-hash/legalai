import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

class GeminiDocumentGenerator:
    def __init__(self, model_name: str = "gemini-3.5-flash"):
        self.model = genai.GenerativeModel(model_name)

    def generate_document(self, document_type: str, parties: str, terms: str, dates: str) -> str:
        prompt = (
            f"Generate a comprehensive, formal legal document titled '{document_type}'.\n"
            f"Involved Parties: {parties}\n"
            f"Effective Date: {dates}\n"
            f"Terms and Conditions: {terms}\n\n"
            f"Ensure formal legal structure with multiple distinct sections, standard legal clauses, "
            f"definitions, obligations, termination conditions, governing law, and designated signature blocks."
        )
        response = self.model.generate_content(prompt)
        return response.text