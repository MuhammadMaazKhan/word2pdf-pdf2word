import os
import subprocess
import streamlit as st
from pdf2docx import Converter

st.set_page_config(page_title="PDF & Word Converter", layout="centered")
st.title("📄 PDF ↔ Word Converter")

tab1, tab2 = st.tabs(["PDF to Word", "Word to PDF"])

# --- PDF TO WORD ---
with tab1:
    st.header("Convert PDF to Word (.docx)")
    uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"])
    
    if uploaded_pdf and st.button("Convert to Word"):
        with st.spinner("Converting..."):
            pdf_path = f"temp_{uploaded_pdf.name}"
            docx_path = pdf_path.replace(".pdf", ".docx")
            
            with open(pdf_path, "wb") as f:
                f.write(uploaded_pdf.getbuffer())
            
            # Convert
            cv = Converter(pdf_path)
            cv.convert(docx_path, start=0, end=None)
            cv.close()
            
            with open(docx_path, "rb") as f:
                st.download_button("📥 Download Word File", f, file_name=os.path.basename(docx_path))
            
            # Cleanup
            if os.path.exists(pdf_path): os.remove(pdf_path)
            if os.path.exists(docx_path): os.remove(docx_path)

# --- WORD TO PDF ---
with tab2:
    st.header("Convert Word (.docx) to PDF")
    uploaded_docx = st.file_uploader("Upload a Word file", type=["docx"])
    
    if uploaded_docx and st.button("Convert to PDF"):
        with st.spinner("Converting..."):
            docx_path = f"temp_{uploaded_docx.name}"
            pdf_path = docx_path.replace(".docx", ".pdf")
            
            with open(docx_path, "wb") as f:
                f.write(uploaded_docx.getbuffer())
            
            # Convert using LibreOffice
            subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', docx_path], check=True)
            
            with open(pdf_path, "rb") as f:
                st.download_button("📥 Download PDF File", f, file_name=os.path.basename(pdf_path))
            
            # Cleanup
            if os.path.exists(docx_path): os.remove(docx_path)
            if os.path.exists(pdf_path): os.remove(pdf_path)
