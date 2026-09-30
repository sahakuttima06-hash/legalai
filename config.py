import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-1.5-pro"

if not GEMINI_API_KEY:
    print("Warning: GEMINI_API_KEY is not set in the .env file.")