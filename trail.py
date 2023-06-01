import streamlit as st
import PyPDF2
# Display a file uploader widget
uploaded_files = st.file_uploader("Upload PDF file", accept_multiple_files=True)
def show_pdf(file_path):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
# Check if a file has been uploaded
if uploaded_files is not None:
    for file in uploaded_files:
        show_pdf(file)
