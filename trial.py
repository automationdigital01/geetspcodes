import streamlit as st
#import PyPDF2
from PyPDF2 import PdfFileReader 
# Display a file uploader widget
uploaded_files = st.file_uploader("Upload PDF file", accept_multiple_files=True, type="pdf")
def read_pdf(file):
	pdfReader = PdfFileReader(file)
	count = pdfReader.numPages
	all_page_text = ""
	for i in range(count):
		page = pdfReader.getPage(i)
		all_page_text += page.extractText()

	return all_page_text

# Check if files have been uploaded
if uploaded_files:
    st.write("Uploaded files:")

    # Iterate through the uploaded files
    for uploaded_file in uploaded_files:
        # Read the file contents
        file_contents = read_pdf(uploaded_file)

        # Display the file name and contents
        st.write("File name:", uploaded_file.name)
        st.write("File contents:")
        st.write(file_contents)
        st.write("---")  # Add a separator between files

   
