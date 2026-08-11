import os
import docx
from reportlab.pdfgen import canvas
from utils import (
    extract_from_txt,
    extract_from_docx,
    extract_from_pdf,
    detect_and_extract,
    fallback_extractive_summarize
)

SAMPLES_DIR = os.path.join(os.path.dirname(__file__), "samples")
os.makedirs(SAMPLES_DIR, exist_ok=True)

def test_fast():
    print("--- 1. Testing .txt Extraction ---")
    txt_path = os.path.join(SAMPLES_DIR, "test.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("Hello World! This is a plain text file test for the text summarizer project.")
    
    text, warn = detect_and_extract(txt_path)
    print(f"Txt Extracted: '{text}' | Warning: {warn}")

    print("\n--- 2. Testing .docx Extraction ---")
    docx_path = os.path.join(SAMPLES_DIR, "test.docx")
    doc = docx.Document()
    doc.add_paragraph("This is a Word document paragraph test.")
    doc.save(docx_path)
    
    text_docx, warn_docx = detect_and_extract(docx_path)
    print(f"Docx Extracted: '{text_docx}' | Warning: {warn_docx}")

    print("\n--- 3. Testing Text-based .pdf Extraction ---")
    pdf_path = os.path.join(SAMPLES_DIR, "test.pdf")
    c = canvas.Canvas(pdf_path)
    c.drawString(100, 700, "This is a text PDF document test for pdfplumber extraction.")
    c.save()

    text_pdf, warn_pdf = detect_and_extract(pdf_path)
    print(f"PDF Extracted: '{text_pdf}' | Warning: {warn_pdf}")

    print("\n--- 4. Testing Extractive Summarizer Fallback ---")
    sample_text = (
        "Artificial intelligence and machine learning have revolutionized text processing. "
        "Modern neural network architectures allow automated summarization of long documents into concise key insights. "
        "This project extends input format support to include Word documents, PDFs, and handwritten notes."
    )
    summary = fallback_extractive_summarize(sample_text, num_sentences=2)
    print(f"Extractive Summary Output: '{summary}'")

if __name__ == "__main__":
    test_fast()
