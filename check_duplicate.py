#import os
#from pathlib import Path
from filecmp2 import cmp_contents
import streamlit as st

# list all documents
#DATA_DIR = Path('C:\\Users\\gpandey2\\Desktop\\construction project\\pdf')
#files = sorted(os.listdir(DATA_DIR))
files=st.uploader("upload files", accept_multiple_files=True)
# list containing the classes of documents with the same content
duplicates = []

# comparison of the documents
for file in files:
    
    is_duplicate = False
    
    for class_ in duplicates:
        is_duplicate = cmp_contents(
            file,
            class_[0]
        )
        if is_duplicate:
            class_.append(file)
            break
    
    if not is_duplicate:
        duplicates.append([file])     

# show results
st.write(duplicates)
