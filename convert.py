import os
import io
import zipfile
import subprocess
import streamlit as st
from pdf2docx import Converter

st.set_page_config(page_title="Batch PDF & Word Converter", layout="centered")
st.title("📄 Batch PDF ↔ Word Converter")

tab1, tab2 = st.tabs(["PDF to Word (ZIP)", "Word to PDF (ZIP)"])

# --- BATCH PDF TO WORD ---
with tab1:
    st.header("Convert Multiple PDFs to Word (.docx)")
    uploaded_pdfs = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)
    
    if uploaded_pdfs and st.button("Convert All PDFs to Word"):
        with st.spinner(f"Converting {len(uploaded_pdfs)} PDF(s)..."):
            zip_buffer = io.BytesIO()
            
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for uploaded_pdf in uploaded_pdfs:
                    pdf_path = f"temp_{uploaded_pdf.name}"
                    docx_name = f"{os.path.splitext(uploaded_pdf.name)[0]}.docx"
                    docx_path = f"temp_{docx_name}"
                    
                    # Save input PDF
                    with open(pdf_path, "wb") as f:
                        f.write(uploaded_pdf.getbuffer())
                    
                    # Convert PDF -> DOCX
                    try:
                        cv = Converter(pdf_path)
                        cv.convert(docx_path, start=0, end=None)
                        cv.close()
                        
                        # Add converted DOCX to ZIP archive
                        zip_file.write(docx_path, arcname=docx_name)
                    except Exception as e:
                        st.error(f"Error converting {uploaded_pdf.name}: {e}")
                    
                    # Clean up temporary files
                    if os.path.exists(pdf_path): os.remove(pdf_path)
                    if os.path.exists(docx_path): os.remove(docx_path)
            
            zip_buffer.seek(0)
            st.success("All PDFs converted successfully!")
            st.download_button(
                label="📥 Download All Converted Word Files (.ZIP)",
                data=zip_buffer,
                file_name="converted_word_files.zip",
                mime="application/zip"
            )

# --- BATCH WORD TO PDF ---
with tab2:
    st.header("Convert Multiple Word (.docx) Files to PDF")
    uploaded_docs = st.file_uploader("Upload Word files", type=["docx"], accept_multiple_files=True)
    
    if uploaded_docs and st.button("Convert All Word Files to PDF"):
        with st.spinner(f"Converting {len(uploaded_docs)} Word document(s)..."):
            zip_buffer = io.BytesIO()
            
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for uploaded_doc in uploaded_docs:
                    docx_path = f"temp_{uploaded_doc.name}"
                    pdf_name = f"{os.path.splitext(uploaded_doc.name)[0]}.pdf"
                    pdf_path = f"temp_{pdf_name}"
                    
                    # Save input DOCX
                    with open(docx_path, "wb") as f:
                        f.write(uploaded_doc.getbuffer())
                    
                    # Convert DOCX -> PDF via LibreOffice
                    try:
                        subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', docx_path], check=True)
                        
                        # LibreOffice creates temp_<name>.pdf in the current directory
                        generated_pdf = docx_path.replace(".docx", ".pdf")
                        
                        # Add to ZIP archive under original name
                        zip_file.write(generated_pdf, arcname=pdf_name)
                        
                        if os.path.exists(generated_pdf): os.remove(generated_pdf)
                    except Exception as e:
                        st.error(f"Error converting {uploaded_doc.name}: {e}")
                    
                    # Clean up temporary file
                    if os.path.exists(docx_path): os.remove(docx_path)
            
            zip_buffer.seek(0)
            st.success("All Word files converted successfully!")
            st.download_button(
                label="📥 Download All Converted PDF Files (.ZIP)",
                data=zip_buffer,
                file_name="converted_pdf_files.zip",
                mime="application/zip"
            )
