import streamlit as st

# Display a file uploader widget
uploaded_file = st.file_uploader("Upload PDF file", type=["pdf"])

# Check if a file has been uploaded
if uploaded_file is not None:
    # Read the file contents
    file_contents = uploaded_file.read()

    # Display the file contents
    st.write("File contents:")
    st.write(file_contents)
