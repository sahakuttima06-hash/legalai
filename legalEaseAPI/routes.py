import sys
import os
from fastapi import APIRouter
from pydantic import BaseModel

# Add project root directory to sys.path so ai_core can be imported from legalEaseAPI
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter()
gemini_generator = GeminiDocumentGenerator()

class DocumentRequest(BaseModel):
    document_type: str
    parties: str
    terms: str
    dates: str

@router.post("/generate")
def generate_legal_document(request: DocumentRequest):
    response = gemini_generator.generate_document(
        request.document_type,
        request.parties,
        request.terms,
        request.dates
    )
    return {"document": response}