# pyrefly: ignore [missing-import]
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

def generate_pdf(text_content):
    """
    Generates a PDF file from markdown/text content using ReportLab.
    Returns a BytesIO object containing the PDF.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    Story = []
    
    # Very basic parsing of the text content for the PDF.
    # In a full implementation, you'd want to parse markdown properly.
    for line in text_content.split('\n'):
        if line.strip():
            # If line is a header (starts with #)
            if line.startswith('#'):
                p = Paragraph(line.replace('#', '').strip(), styles['Heading1'])
            elif line.startswith('-') or line.startswith('*'):
                p = Paragraph(line, styles['Normal'])
            else:
                p = Paragraph(line, styles['Normal'])
            Story.append(p)
            Story.append(Spacer(1, 0.1 * 72))  # Add a little space
            
    doc.build(Story)
    buffer.seek(0)
    return buffer
