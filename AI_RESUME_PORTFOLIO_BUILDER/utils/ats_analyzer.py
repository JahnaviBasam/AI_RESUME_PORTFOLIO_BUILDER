# pyrefly: ignore [missing-import]
import fitz  # PyMuPDF
from .gemini_api import check_ats_score
import json
import re

def extract_text_from_pdf(pdf_buffer):
    """
    Extracts text from a PyMuPDF supported PDF buffer.
    """
    try:
        doc = fitz.open(stream=pdf_buffer, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

def analyze_resume_ats(pdf_buffer, job_description=""):
    """
    Extracts text and queries Gemini for ATS analysis.
    Returns a dictionary of the results.
    """
    resume_text = extract_text_from_pdf(pdf_buffer)
    
    if "Error reading PDF" in resume_text:
        return {"error": resume_text}
        
    ai_response = check_ats_score(resume_text, job_description)
    
    # Try to parse the JSON response from Gemini
    try:
        # Extract json content if wrapped in markdown
        json_match = re.search(r'```json\n(.*?)\n```', ai_response, re.DOTALL)
        if json_match:
            ai_response = json_match.group(1)
        return json.loads(ai_response)
    except Exception as e:
        # Fallback if the AI didn't return perfect JSON
        return {
            "error": "Failed to parse AI response as JSON.",
            "raw_response": ai_response
        }
