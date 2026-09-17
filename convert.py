import os
import subprocess
from pdf2docx import Converter

def convert_pdf_to_docx(pdf_file, docx_file):
    """Converts a PDF file to DOCX format using pdf2docx."""
    try:
        cv = Converter(pdf_file)
        cv.convert(docx_file, start=0, end=None)
        cv.close()
        print(f"Successfully converted PDF: {pdf_file} -> {docx_file}")
    except Exception as e:
        print(f"Error converting PDF {pdf_file}: {e}")

def convert_docx_to_pdf(docx_file, output_folder):
    """Converts a DOCX file to PDF using headless LibreOffice."""
    try:
        subprocess.run(
            ['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', output_folder, docx_file],
            check=True
        )
        print(f"Successfully converted DOCX: {docx_file} to PDF")
    except Exception as e:
        print(f"Error converting DOCX {docx_file}: {e}")

def process_conversions():
    # Make sure target directories exist
    os.makedirs("pdf_to_word/input", exist_ok=True)
    os.makedirs("pdf_to_word/output", exist_ok=True)
    os.makedirs("word_to_pdf/input", exist_ok=True)
    os.makedirs("word_to_pdf/output", exist_ok=True)

    # 1. Convert PDFs to DOCX
    pdf_dir = "pdf_to_word/input"
    for filename in os.listdir(pdf_dir):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(pdf_dir, filename)
            docx_path = os.path.join("pdf_to_word/output", f"{os.path.splitext(filename)[0]}.docx")
            convert_pdf_to_docx(pdf_path, docx_path)

    # 2. Convert DOCX to PDF
    word_dir = "word_to_pdf/input"
    for filename in os.listdir(word_dir):
        if filename.lower().endswith(".docx"):
            docx_path = os.path.join(word_dir, filename)
            output_folder = "word_to_pdf/output"
            convert_docx_to_pdf(docx_path, output_folder)

if __name__ == "__main__":
    process_conversions()
