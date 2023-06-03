import streamlit as st
import spacy
import gdown
import zipfile
import pandas as pd
import re
import nltk
from nltk import ne_chunk, pos_tag, word_tokenize, download
from spacy.matcher import PhraseMatcher
import matplotlib.pyplot as plt
import seaborn as sns
import pdfplumber

def read_pdf_with_pdfplumber(file):
    with pdfplumber.open(file) as pdf:
        page = pdf.pages[0]
        return page.extract_text()

def predict(filepaths, nlp):
    entities_list = []
    for filepath in filepaths:
        file_contents=filepath
        #file_contents = filepath.decode('utf-8')
        email = None
        name = None
        roles = None
        education = None
        phone_number = None
        degree = None
        skills= None
        

        doc = nlp(file_contents)
        for ent in doc.ents:
            if ent.label_ == "EMAIL" and email is None:
                email = ent.text
            elif ent.label_ == "PERSON" and name is None:
                name = ent.text
            elif ent.label_ == "ROLES" and roles is None:
                roles = ent.text
            elif ent.label_ == "EDUCATION" and education is None:
                education = ent.text
            elif ent.label_ == "PHONE NUMBER" and phone_number is None:
                phone_number = ent.text
            elif ent.label_ == "DEGREE" and degree is None:
                degree = ent.text
            elif ent.label_ == "SKILLS" and skills is None:
                skills = ent.text


            entities_list.append({
            "Email": email,
            "Name": name,
            "Roles": roles,
            "Education": education,
            "Phone Number": phone_number,
            "Degree": degree,
            "Skills": skills
        })

    return pd.DataFrame(entities_list)

st.set_option('deprecation.showPyplotGlobalUse', False)

def perform_education_analysis(df):
    roles_counts = df['Roles'].value_counts()
    roles_levels = roles_counts.index.tolist()
    counts = roles_counts.values.tolist()

    # Plot the bar chart
    plt.figure(figsize=(12, 8))
    sns.barplot(x=counts, y=roles_levels, palette='cool')
    plt.xlabel('Count')
    plt.ylabel('Roles Level')
    plt.title('Roles Distribution')
    st.pyplot() 

    # Plot the pie chart
    #roles_counts = df['Roles'].value_counts()
    #education_levels = education_counts.index.tolist()
    #ecounts = education_counts.values.tolist()
    plt.figure(figsize=(12, 8))
    plt.pie(counts, labels=roles_levels, colors=sns.color_palette('cool'), autopct='%.0f%%')
    plt.title('Roles Distribution')
    st.pyplot()

def main():
    st.title("Resume Parser")
    uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True)
    #option = st.selectbox('file type',('text','pdf'))
    result = st.button("Get result")

    if result and uploaded_files is not None:
        model_url = "https://drive.google.com/uc?id=1z5iNtXPVsDWs4kNT83UMrFVYf7c2wFxO" 
        output_file = "model.zip"
        gdown.download(model_url, output_file, quiet=False)

        with zipfile.ZipFile(output_file, "r") as zip_ref:
            zip_ref.extractall("model")

        model_path = "./model"
        nlp = spacy.load(model_path)
        

        text=[]
        for uploaded_file in uploaded_files:
            if uploaded_file.name.endswith(".pdf"):
                pdf_contents = read_pdf_with_pdfplumber(uploaded_file)
                text.append(pdf_contents)
            else:
                text.append(uploaded_file)
                       
        df = predict(text, nlp)

        st.write("Parsed Resumes:")
        st.dataframe(df[["Email", "Name", "Roles", "Education", "Phone Number", "Degree", "Skills"]])
        perform_education_analysis(df)


if __name__ == "__main__":
        main()
