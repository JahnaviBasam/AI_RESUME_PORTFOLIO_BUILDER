# pyrefly: ignore [missing-import]
import streamlit as st
import os
import sys

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.gemini_api import get_interview_prep

# Load custom CSS
def load_css():
    css_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "style.css")
    if os.path.exists(css_file):
        with open(css_file, "r") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

st.title("🎤 AI Interview Prep")
st.write("Generate tailored interview questions based on your resume and target role.")

with st.form("interview_prep_form"):
    role = st.text_input("Target Role (e.g. Data Analyst, Frontend Developer)")
    resume_text = st.text_area("Your Resume Summary or Key Skills", height=150)
    
    submit = st.form_submit_button("✨ Generate Interview Questions")

if submit:
    if not role or not resume_text:
        st.error("Please provide both the Target Role and Resume summary.")
    else:
        with st.spinner("AI is analyzing your profile to generate questions..."):
            prep_material = get_interview_prep(role, resume_text)
            st.session_state['interview_prep'] = prep_material
            st.success("Questions generated!")

if 'interview_prep' in st.session_state:
    st.markdown("### 📝 Your Tailored Interview Guide")
    st.markdown(st.session_state['interview_prep'])
