import os
import zipfile
import io
from .gemini_api import get_gemini_model

def generate_portfolio_code(name, role, about, skills, projects, links, theme="Modern Dark"):
    """
    Uses Gemini to generate a complete, responsive single-page HTML portfolio.
    """
    prompt = f"""
    You are an expert web developer and UI/UX designer.
    Create a complete, responsive, single-page personal portfolio website (HTML, CSS, JS combined in one file) for the following person.
    
    Name: {name}
    Role: {role}
    About: {about}
    Skills: {skills}
    Projects: {projects}
    Links (GitHub, LinkedIn, etc.): {links}
    
    Theme: {theme} (Use modern design principles, glassmorphism if applicable, animations, responsive flexbox/grid).
    
    CRITICAL:
    1. Provide ONLY valid HTML code. No markdown wrapping (like ```html), just the raw code starting with <!DOCTYPE html>.
    2. Include CSS in a <style> tag and JS in a <script> tag.
    3. Make it look extremely premium, professional, and visually stunning.
    """
    
    try:
        model = get_gemini_model()
        response = model.generate_content(prompt)
        html_content = response.text
        
        # Clean up if the model includes markdown backticks despite instructions
        if html_content.startswith("```html"):
            html_content = html_content.replace("```html", "", 1)
        if html_content.endswith("```"):
            html_content = html_content.rsplit("```", 1)[0]
            
        return html_content.strip()
    except Exception as e:
        return f"<h1>Error generating portfolio: {e}</h1>"

def create_portfolio_zip(html_content):
    """
    Creates a zip file containing the generated portfolio index.html
    Returns a BytesIO object.
    """
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.writestr('index.html', html_content)
        # You could also parse out CSS/JS to separate files here if desired.
    
    buffer.seek(0)
    return buffer
