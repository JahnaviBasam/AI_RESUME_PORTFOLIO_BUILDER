# pyrefly: ignore [missing-import]
import streamlit as st
# pyrefly: ignore [missing-import]
import streamlit.components.v1 as components
import os
import sys

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.portfolio_builder import generate_portfolio_code, create_portfolio_zip

# Load custom CSS
def load_css():
    css_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "style.css")
    if os.path.exists(css_file):
        with open(css_file, "r") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

st.title("🌐 AI Portfolio Generator")
st.write("Generate a stunning, responsive personal portfolio website in seconds.")

with st.form("portfolio_form"):
    st.subheader("Your Details")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name")
        role = st.text_input("Headline / Role (e.g., Full Stack Developer)")
    with col2:
        links = st.text_input("Social Links (GitHub, LinkedIn, Twitter)")
        theme = st.selectbox("Portfolio Theme", ["Dark Modern", "Minimalist White", "Neon Cyberpunk", "Creative Glassmorphism"])
        
    about = st.text_area("About Me", height=100)
    skills = st.text_input("Top Skills (comma separated)")
    projects = st.text_area("Featured Projects (Briefly describe 2-3 projects)", height=150)
    
    submit = st.form_submit_button("✨ Generate Portfolio")

if submit:
    if not name or not role:
        st.error("Name and Role are required.")
    else:
        with st.spinner("AI is designing and coding your portfolio..."):
            html_code = generate_portfolio_code(name, role, about, skills, projects, links, theme)
            st.session_state['portfolio_html'] = html_code
            st.success("Portfolio generated successfully!")

if 'portfolio_html' in st.session_state:
    st.markdown("### 🖥️ Live Preview")
    
    # Display the generated HTML in an iframe
    components.html(st.session_state['portfolio_html'], height=600, scrolling=True)
    
    st.markdown("### 💾 Download Source Code")
    zip_buffer = create_portfolio_zip(st.session_state['portfolio_html'])
    
    st.download_button(
        label="⬇️ Download Website (.zip)",
        data=zip_buffer,
        file_name=f"{name.replace(' ', '_')}_portfolio.zip" if name else "portfolio.zip",
        mime="application/zip"
    )
    
    with st.expander("View Raw HTML/CSS"):
        st.code(st.session_state['portfolio_html'], language="html")
