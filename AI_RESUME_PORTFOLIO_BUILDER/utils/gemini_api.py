import os
import google.generativeai as genai
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the API key
# Expects GEMINI_API_KEY to be set in .env or system environment
API_KEY = os.environ.get("USE_YOUR_GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    print("Warning: USE_YOUR_GEMINI_API_KEY not found. AI features will not work.")

# Use the recommended Gemini model
MODEL_NAME = "gemini-1.5-flash"  # Defaulting to flash for faster responses, can switch to pro

def get_gemini_model():
    return genai.GenerativeModel(MODEL_NAME)

def generate_resume_content(user_info, role, tone="Professional"):
    """
    Generates a professional resume based on user info.
    """
    prompt = f"""
    You are an expert resume writer and career coach.
    Based on the following user information, create a well-structured, ATS-friendly resume tailored for the role of '{role}'.
    The tone should be {tone}.

    User Information:
    {user_info}

    Format the output in clear Markdown with the following sections:
    - Career Objective
    - Technical Skills
    - Experience / Internships (Rewrite bullet points to be impactful and measurable)
    - Projects (Highlight technologies used and outcomes)
    - Education
    - Certifications / Achievements
    """
    try:
        model = get_gemini_model()
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating content: {e}"

def check_ats_score(resume_text, job_description=""):
    """
    Analyzes the resume text and calculates an ATS score.
    """
    prompt = f"""
    You are an Applicant Tracking System (ATS) and expert Recruiter.
    Analyze the following resume. If a job description is provided, analyze the match.
    
    Resume Text:
    {resume_text}

    Job Description (Optional):
    {job_description}

    Provide your response strictly in the following JSON format:
    {{
        "ats_score": <number between 0 and 100>,
        "missing_keywords": ["keyword1", "keyword2"],
        "formatting_issues": ["issue1", "issue2"],
        "suggestions": ["suggestion1", "suggestion2"],
        "strength_summary": "Short summary of resume strength"
    }}
    """
    try:
        model = get_gemini_model()
        response = model.generate_content(prompt)
        # In a real app, you would parse the JSON safely
        return response.text
    except Exception as e:
        return f"{{'error': '{str(e)}'}}"

def generate_cover_letter(resume_text, company_name, job_role, job_description):
    """
    Generates a cover letter tailored to a specific job and company.
    """
    prompt = f"""
    You are an expert career coach. Write a compelling, professional cover letter.
    
    Company: {company_name}
    Role: {job_role}
    
    Job Description:
    {job_description}
    
    Candidate's Resume/Details:
    {resume_text}
    
    Write a 3-4 paragraph cover letter that highlights why the candidate is a perfect fit for the role based on their resume. DO NOT just repeat the resume. Focus on the value they bring to {company_name}.
    """
    try:
        model = get_gemini_model()
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating cover letter: {e}"

def enhance_project_description(description):
    """
    Rewrites a rough project description into a professional, impact-driven format.
    """
    prompt = f"""
    Rewrite the following project description to make it professional, impactful, and ATS-friendly.
    Highlight technologies used and focus on measurable outcomes. Give two versions: a concise bullet point and a detailed paragraph.

    Original Description:
    {description}
    """
    try:
        model = get_gemini_model()
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error enhancing project: {e}"

def get_interview_prep(role, resume_text):
    """
    Generates interview questions based on role and resume.
    """
    prompt = f"""
    You are a technical interviewer and HR manager.
    Generate interview preparation material for the role of '{role}' based on the candidate's resume.
    
    Resume:
    {resume_text}
    
    Provide:
    1. 3 Technical Questions (based on their skills)
    2. 2 Behavioral Questions
    3. 1 HR Question
    Include suggested talking points or tips for answering each.
    """
    try:
        model = get_gemini_model()
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating interview prep: {e}"
