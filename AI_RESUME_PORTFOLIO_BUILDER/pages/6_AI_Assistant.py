# pyrefly: ignore [missing-import]
import streamlit as st
import os
import sys

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.gemini_api import get_gemini_model

# Load custom CSS
def load_css():
    css_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "style.css")
    if os.path.exists(css_file):
        with open(css_file, "r") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

st.title("🤖 AI Career Assistant")
st.write("Chat with your personal career assistant for advice on resumes, interviews, or career paths.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm your AI Career Assistant. How can I help you today? You can ask me to review a project description, suggest skills, or give interview tips."}
    ]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask me anything about your career..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Prepare context for the API
    # Combine past messages (limited to last few for context length)
    context = ""
    for msg in st.session_state.messages[-5:]:
        context += f"{msg['role'].capitalize()}: {msg['content']}\n"
        
    full_prompt = f"""
    You are a friendly, expert career coach and AI assistant.
    Use the following conversation context to answer the user's latest question.
    
    Context:
    {context}
    
    Respond directly to the user's latest query in a professional, helpful tone.
    """

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                model = get_gemini_model()
                response = model.generate_content(full_prompt)
                ai_response = response.text
                st.markdown(ai_response)
            except Exception as e:
                ai_response = f"I encountered an error: {e}"
                st.error(ai_response)
                
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
