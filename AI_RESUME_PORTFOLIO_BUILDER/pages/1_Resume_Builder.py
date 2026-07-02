# pyrefly: ignore [missing-import]
import streamlit as st
import os
import sys

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.gemini_api import generate_resume_content
from utils.pdf_generator import generate_pdf
from utils.docx_generator import generate_docx

# Load custom CSS
def load_css():
    css_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "style.css")
    if os.path.exists(css_file):
        with open(css_file, "r") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

st.title("📄 AI Resume Generator")
st.write("Fill in your details below and let AI craft a professional, ATS-optimized resume for you.")

with st.form("resume_form"):
    st.subheader("Personal Information")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        github = st.text_input("GitHub URL")
    with col2:
        phone = st.text_input("Phone Number")
        linkedin = st.text_input("LinkedIn URL")
        portfolio = st.text_input("Portfolio URL")

    st.subheader("Target Role & Tone")
    col3, col4 = st.columns(2)
    with col3:
        role = st.text_input("Target Job Role", placeholder="e.g., Software Engineer, Data Scientist")
    with col4:
        tone = st.selectbox("Resume Tone", ["Professional", "Technical", "Creative", "Executive"])

    st.subheader("Experience & Education")
    experience = st.text_area("Experience / Internships", placeholder="List your work experience. Don't worry about perfect wording, AI will enhance it.", height=150)
    education = st.text_area("Education", placeholder="University, Degree, Graduation Year, GPA")
    
    st.subheader("Skills & Projects")
    skills = st.text_input("Technical Skills", placeholder="Comma separated (e.g., Python, React, SQL)")
    projects = st.text_area("Projects", placeholder="Describe your key projects and what you built.", height=150)

    st.subheader("Additional Info")
    certifications = st.text_area("Certifications & Achievements")

    submit = st.form_submit_button("✨ Generate AI Resume")

if submit:
    if not name or not role:
        st.error("Please provide at least your Name and Target Job Role.")
    else:
        with st.spinner("AI is crafting your perfect resume..."):
            user_info = f"""
            Name: {name}
            Email: {email}, Phone: {phone}
            Links: {linkedin}, {github}, {portfolio}
            
            Skills: {skills}
            
            Experience:
            {experience}
            
            Projects:
            {projects}
            
            Education:
            {education}
            
            Certifications/Achievements:
            {certifications}
            """
            
            # Call Gemini
            generated_resume = generate_resume_content(user_info, role, tone)
            
            st.session_state['generated_resume'] = generated_resume
            st.success("Resume generated successfully!")

if 'generated_resume' in st.session_state:
    st.markdown("### Your AI-Generated Resume")
    
    # Allow user to edit the generated markdown before exporting
    edited_resume = st.text_area("Review and Edit Your Resume", st.session_state['generated_resume'], height=400)
    
    col_dl1, col_dl2 = st.columns(2)
    
    with col_dl1:
        pdf_buffer = generate_pdf(edited_resume)
        st.download_button(
            label="⬇️ Download PDF",
            data=pdf_buffer,
            file_name=f"{name.replace(' ', '_')}_Resume.pdf" if name else "Resume.pdf",
            mime="application/pdf"
        )
        
    with col_dl2:
        docx_buffer = generate_docx(edited_resume)
        st.download_button(
            label="⬇️ Download DOCX",
            data=docx_buffer,
            file_name=f"{name.replace(' ', '_')}_Resume.docx" if name else "Resume.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
