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

def extract_education(txt):
    education=[
        'chemical engineering',
        'computer science engineering',
        'mechanical engineering',
        'electrical engineering',
        'civil engineering',
        'LLB',
        'CA',
        'Law',
        'engineering'
    ]
    extracted_education = []
    
    for idx in education:
        if idx.lower() in txt.lower():
            extracted_education.append(idx)
    
    return extracted_education

def extract_degree(txt):
    degrees = [       
        'Btech',
        'BE',
        'Mtech',
        'MS',
        'BSc',
        'MSc',
        'Diploma',
        'Phd',
        'LLB',
        'BA-LLB',
        'CA',
        'MBA'
    ]
    
    extracted_degrees = []
    
    for degree in degrees:
        if degree.lower() in txt.lower():
            extracted_degrees.append(degree)
    
    return extracted_degrees

def extract_skills(txt):
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
    
    extracted_skills = []
    
    for skill in skills:
        if skill.lower() in txt.lower():
            extracted_skills.append(skills)
    
    return extracted_skills

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
            elif ent.label_ == "NAME" and name is None:
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
                
        if education is None or education == "NA":
            extracted_education = extract_education(file_contents)
            if extracted_education:
                degree = extracted_education[0] 
                
        if skills is None or skills == "NA":
            extracted_skills = extract_skills(file_contents)
            if extracted_skills:
                skills = extracted_skills[0]             

        

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

@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')    

    
    
def main():
    #st.title("Resume Parser")
    #uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True)
    #option = st.selectbox('file type',('text','pdf'))
    #result = st.button("Get result")

    if uploaded_files is not None:
        model_url = "https://drive.google.com/uc?id=1z5iNtXPVsDWs4kNT83UMrFVYf7c2wFxO" 
        output_file = "model-best.zip"
        gdown.download(model_url, output_file, quiet=False)

        with zipfile.ZipFile(output_file, "r") as zip_ref:
            zip_ref.extractall("model-best")

        model_path = "./model-best"
        nlp = spacy.load(model_path)
        

        text=[]
        for uploaded_file in uploaded_files:
            if uploaded_file.name.endswith(".pdf"):
                pdf_contents = read_pdf_with_pdfplumber(uploaded_file)
                text.append(pdf_contents)
            else:
                text = uploaded_file.decode('utf-8')
                text.append(file)
        df = predict(text, nlp)
        df=df.astype(str)
        df.to_feather('df')

        st.write("Parsed Resumes:")
        st.dataframe(df[["Email", "Name", "Roles", "Education", "Phone Number", "Degree", "Skills"]])
        perform_education_analysis(df)
        
        csv = df.to_csv().encode('utf-8')

        st.download_button(label="Download data as CSV",
                           data=csv,
                           file_name='cv_df.csv',
                           mime='text/csv',)
                               
  

if __name__ == "__main__":
    download('words')
    nltk.download('maxent_ne_chunker')
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    st.title("Resume Parser")
    uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True)
    main()
    
