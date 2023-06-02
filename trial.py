import streamlit as st
import PyPDF2
# Display a file uploader widget
uploaded_files = st.file_uploader("Upload PDF file", accept_multiple_files=True, type="pdf")

    # Check if a file has been uploaded
if uploaded_files is not None:
    for file in uploaded_files:
        base64_pdf = base64.b64encode(file.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
