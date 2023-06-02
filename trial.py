import streamlit as st
import PyPDF2
# Display a file uploader widget
uploaded_files = st.file_uploader("Upload PDF file", accept_multiple_files=True, type="pdf")


# Check if files have been uploaded
if uploaded_files:
    st.write("Uploaded files:")

    # Iterate through the uploaded files
    for uploaded_file in uploaded_files:
        # Read the file contents
        file_contents = uploaded_file.read()

        # Display the file name and contents
        st.write("File name:", uploaded_file.name)
        st.write("File contents:")
        st.write(file_contents)
        st.write("---")  # Add a separator between files

   
