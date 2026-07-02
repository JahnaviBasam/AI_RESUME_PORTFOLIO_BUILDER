# pyrefly: ignore [missing-import]
import streamlit as st
import os

# Configure the Streamlit page
st.set_page_config(
    page_title="AI Resume & Portfolio Builder",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    css_file = os.path.join(os.path.dirname(__file__), "assets", "style.css")
    if os.path.exists(css_file):
        with open(css_file, "r") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    else:
        st.warning("Custom CSS not found.")

load_css()

# Sidebar Navigation (Streamlit automatically uses the pages/ folder for multi-page apps, 
# but we can add some branding here)
st.sidebar.markdown("""
<div style="text-align: center; margin-bottom: 20px;">
    <h2>✨ AI Builder</h2>
    <p style="color: #a855f7; font-size: 0.9rem;">Next-Gen Career Tools</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.info("Select a tool from the menu above to get started.")

# Main Dashboard Layout
st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h1 style="font-size: 3.5rem; background: linear-gradient(90deg, #a855f7, #6366f1); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        AI Resume & Portfolio Builder
    </h1>
    <p style="font-size: 1.2rem; color: #cbd5e1; max-width: 600px; margin: 0 auto;">
        Supercharge your career with AI-driven resumes, tailored cover letters, and stunning portfolio websites designed to beat the ATS and wow recruiters.
    </p>
</div>
""", unsafe_allow_html=True)

# Dashboard Features Grid
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="glass-card">
        <h3>📄 AI Resume Generator</h3>
        <p style="color: #94a3b8; font-size: 0.9rem;">Generate professional, ATS-friendly resumes tailored to your role. Let Gemini rewrite your bullet points for maximum impact.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card">
        <h3>🔍 ATS Checker</h3>
        <p style="color: #94a3b8; font-size: 0.9rem;">Upload your resume and get an instant ATS score. Identify missing keywords and fix formatting issues before you apply.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-card">
        <h3>✉️ Cover Letter AI</h3>
        <p style="color: #94a3b8; font-size: 0.9rem;">Create personalized, compelling cover letters based on the specific job description and your unique skills in seconds.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card">
        <h3>🌐 Portfolio Builder</h3>
        <p style="color: #94a3b8; font-size: 0.9rem;">Automatically generate a responsive, modern personal website with live preview and downloadable source code.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="glass-card">
        <h3>🎤 Interview Prep</h3>
        <p style="color: #94a3b8; font-size: 0.9rem;">Get tailored interview questions (technical, behavioral, HR) based on your target role and resume, complete with suggested answers.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
        <h3>🤖 AI Chat Assistant</h3>
        <p style="color: #94a3b8; font-size: 0.9rem;">Chat with your personal career assistant. Ask for advice, resume improvements, or industry insights in real-time.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b; font-size: 0.8rem;'>Powered by Google Gemini API & Streamlit</p>", unsafe_allow_html=True)

