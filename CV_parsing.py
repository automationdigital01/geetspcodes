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


def extract_names(txt):
    person_names = []
    for sent in nltk.sent_tokenize(txt):
        for chunk in ne_chunk(pos_tag(word_tokenize(sent))):
            if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                person_names.append(' '.join(chunk_leave[0] for chunk_leave in chunk.leaves()))
    return person_names

def extract_emails(txt):
    emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", txt)
    return emails

def get_phone_numbers(txt):
    r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    phone_numbers = r.findall(txt)
    return [re.sub(r'\D', '', num) for num in phone_numbers]

def extract_skills(txt, skills, nlp):
    skill_set = set()
    matcher = PhraseMatcher(nlp.vocab)
    patterns = [nlp(skill) for skill in skills]
    matcher.add("SKILLS", None, *patterns)
    doc = nlp(txt)
    matches = matcher(doc)
    for match_id, start, end in matches:
        skill = doc[start:end].text
        skill_set.add(skill)
    return list(skill_set)

def extract_degree(txt):
    degrees = [
       
        "M.Tech Chemical",
        "BE Chemical",
        "BTech",
        "B. Tech",
        "M.Chem.Engg.",
        "B.E (Chemical)",
        "B.E(EEE)",
        "Bachelor of Technology - Chemical Engineering" ,
        "B.E. Mechanical",
        "B.E. MECHANICAL",
        "Mtech",
        "B. Tech/B. E In Electrical and Electronics Engineering",
        "B.E. -Chemical Engineering",
        "Postgraduate"
    ]
    
    extracted_degrees = []
    
    for degree in degrees:
        if degree.lower() in txt.lower():
            extracted_degrees.append(degree)
    
    return extracted_degrees

def predict(filepaths, nlp, skills):
    entities_list = []

    for filepath in filepaths:
        file_contents = filepath.read().decode('utf-8')
        email = None
        name = None
        roles = None
        education = None
        phone_number = None
        degree = None
        extracted_skills = []

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

        if email is None:
            extracted_emails = extract_emails(file_contents)
            if extracted_emails:
                email = extracted_emails[0]

        if name is None:
            extracted_names = extract_names(file_contents)
            if extracted_names:
                name = extracted_names[0]

        if phone_number is None:
            extracted_phone_numbers = get_phone_numbers(file_contents)
            if extracted_phone_numbers:
                phone_number = extracted_phone_numbers[0]

        if degree is None or degree == "NA":
            extracted_degrees = extract_degree(file_contents)
            if extracted_degrees:
                degree = extracted_degrees[0]

        extracted_skills = extract_skills(file_contents, skills, nlp)

        entities_list.append({
            "Email": email,
            "Name": name,
            "Roles": roles,
            "Education": education,
            "Phone Number": phone_number,
            "Degree": degree,
            "Skills": extracted_skills
        })

    return pd.DataFrame(entities_list)

st.set_option('deprecation.showPyplotGlobalUse', False)

def perform_education_analysis(df):
    education_counts = df['Education'].value_counts()

 
    education_levels = education_counts.index.tolist()
    counts = education_counts.values.tolist()

    # Plot the bar chart
    plt.figure(figsize=(12, 8))
    sns.barplot(x=counts, y=education_levels, palette='cool')
    plt.xlabel('Count')
    plt.ylabel('Education Level')
    plt.title('Education Level Distribution')
    st.pyplot() 

    # Plot the pie chart
    plt.figure(figsize=(12, 8))
    plt.pie(counts, labels=education_levels, colors=sns.color_palette('cool'), autopct='%.0f%%')
    plt.title('Education Level Distribution')
    st.pyplot()

def main():
    st.title("Resume Parser")
    uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True)
    result = st.button("Get result")

    if result and uploaded_files is not None:

        model_url = "https://drive.google.com/file/d/1vUuQpsl-MfsE3m9VELI-0I53qCqXo_bm/view?usp=share_link" 
        output_file = "model-best.zip"
        gdown.download(model_url, output_file, quiet=False)

        with zipfile.ZipFile(output_file, "r") as zip_ref:
            zip_ref.extractall("model")

        model_path = "./model"
        nlp = spacy.load(model_path)

        skills = [
            "SAP",
            "STAAD PRO.",
            "Mat3D",
            "AutoCAD",
            "TEKLA Viewer",
            "Mathcad",
            "MS Office",
            "python",
            "oracle",
            "HYSYS-3.2",
            "HTRI-6.0",
            "ASPEN"
        ]

        df = predict(uploaded_files, nlp, skills)

        st.write("Parsed Resumes:")
        st.dataframe(df[["Email", "Name", "Roles", "Education", "Phone Number", "Degree", "Skills"]], height=len(df))
        perform_education_analysis(df)
        
        

if __name__ == "__main__":
    download('words')
    nltk.download('maxent_ne_chunker')
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    main()
