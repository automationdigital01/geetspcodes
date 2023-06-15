#import os
#from pathlib import Path
from filecmp import cmp
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
        is_duplicate = cmp(
            DATA_DIR / file,
            DATA_DIR / class_[0],
            shallow = False
        )
        if is_duplicate:
            class_.append(file)
            break
    
    if not is_duplicate:
        duplicates.append([file])     

# show results
st.write(duplicates)
