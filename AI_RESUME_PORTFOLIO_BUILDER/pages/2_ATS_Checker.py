# pyrefly: ignore [missing-import]
import streamlit as st
import os
import sys

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.ats_analyzer import analyze_resume_ats

# Load custom CSS
def load_css():
    css_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "style.css")
    if os.path.exists(css_file):
        with open(css_file, "r") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

st.title("🔍 ATS Resume Checker")
st.write("Upload your PDF resume and get an instant AI-powered ATS analysis to improve your chances.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Upload Resume")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

with col2:
    st.subheader("Job Description (Optional)")
    job_desc = st.text_area("Paste the job description here for a tailored match score.", height=150)

if st.button("✨ Analyze Resume"):
    if uploaded_file is not None:
        with st.spinner("AI is analyzing your resume..."):
            pdf_bytes = uploaded_file.read()
            results = analyze_resume_ats(pdf_bytes, job_desc)
            
            if "error" in results:
                st.error(results["error"])
                if "raw_response" in results:
                    st.warning("Raw AI output (could not be formatted perfectly):")
                    st.write(results["raw_response"])
            else:
                st.success("Analysis Complete!")
                
                # Display Score
                score = results.get("ats_score", 0)
                
                # Determine color based on score
                if score >= 80:
                    color = "#22c55e" # Green
                elif score >= 60:
                    color = "#eab308" # Yellow
                else:
                    color = "#ef4444" # Red
                    
                st.markdown(f"""
                <div style="text-align: center; padding: 2rem; background: rgba(255,255,255,0.05); border-radius: 15px; margin-bottom: 2rem;">
                    <h2 style="margin: 0; color: #94a3b8;">ATS Match Score</h2>
                    <h1 style="margin: 0; font-size: 5rem; color: {color};">{score}%</h1>
                    <p style="margin: 0; color: #cbd5e1; font-size: 1.2rem;">{results.get("strength_summary", "")}</p>
                </div>
                """, unsafe_allow_html=True)
                
                c1, c2 = st.columns(2)
                
                with c1:
                    st.markdown("### ⚠️ Missing Keywords / Skills")
                    for kw in results.get("missing_keywords", []):
                        st.markdown(f'<span class="skill-chip">{kw}</span>', unsafe_allow_html=True)
                        
                    st.markdown("### 📝 Formatting Issues")
                    for issue in results.get("formatting_issues", []):
                        st.write(f"- {issue}")
                        
                with c2:
                    st.markdown("### 💡 AI Suggestions for Improvement")
                    for suggestion in results.get("suggestions", []):
                        st.info(suggestion)
    else:
        st.error("Please upload a PDF resume first.")
