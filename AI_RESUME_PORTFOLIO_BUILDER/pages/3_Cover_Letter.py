# pyrefly: ignore [missing-import]
import streamlit as st
import os
import sys

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.gemini_api import generate_cover_letter
from utils.pdf_generator import generate_pdf

# Load custom CSS
def load_css():
    css_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "style.css")
    if os.path.exists(css_file):
        with open(css_file, "r") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

st.title("✉️ AI Cover Letter Generator")
st.write("Generate a personalized, compelling cover letter tailored to a specific job description.")

with st.form("cover_letter_form"):
    st.subheader("Job Details")
    company = st.text_input("Company Name")
    role = st.text_input("Target Role")
    job_desc = st.text_area("Job Description", placeholder="Paste the job description here...", height=150)
    
    st.subheader("Your Information")
    # In a real app, this could be pulled from a database or session state if they already filled the resume builder
    resume_info = st.text_area("Your Resume / Profile Summary", placeholder="Paste your resume text or a summary of your skills and experience here...", height=150)

    submit = st.form_submit_button("✨ Generate Cover Letter")

if submit:
    if not company or not role or not resume_info:
        st.error("Please fill in the Company Name, Target Role, and Your Resume Information.")
    else:
        with st.spinner("Writing your cover letter..."):
            cl_text = generate_cover_letter(resume_info, company, role, job_desc)
            st.session_state['generated_cl'] = cl_text
            st.success("Cover letter generated!")

if 'generated_cl' in st.session_state:
    st.markdown("### Your Cover Letter")
    
    edited_cl = st.text_area("Review and Edit", st.session_state['generated_cl'], height=400)
    
    pdf_buffer = generate_pdf(edited_cl)
    st.download_button(
        label="⬇️ Download PDF",
        data=pdf_buffer,
        file_name=f"Cover_Letter_{company.replace(' ', '_')}.pdf",
        mime="application/pdf"
    )
