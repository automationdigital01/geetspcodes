import streamlit as st
import PyPDF2
# Display a file uploader widget
uploaded_files = st.file_uploader("Upload PDF file", accept_multiple_files=True)

# Check if a file has been uploaded
if uploaded_files is not None:
    for file in uploaded_files:
        with open(, 'rb') as file:
            read=PyPDF2.PdfReader(file)
            pagenum=len(read.pages)
            page_content=read.pages[0]
            text=page_content.extract_text()
            st.write(text)
    
