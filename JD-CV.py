import streamlit as st
import pdfplumber
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#pdf extract 
def read_pdf_with_pdfplumber(file):
  with pdfplumber.open(file) as pdf:
    page = pdf.pages[0]
    return page.extract_text()
  
#clear all commas and spaces in text
def cleartext(text):
  Script=''.join(text)
  Clear=Script.replace("\n","")
  return Clear
      
#similarity check between job description and resumes/cvs
def check_similarity(CV_Clear, JD_Clear):
  Match_Test=[CV_Clear, JD_Clear]
  cv=CountVectorizer()
  count_matrix=cv.fit_transform(Match_Test)
  #print('Similarity is :',cosine_similarity(count_matrix))
  MatchPercentage=cosine_similarity(count_matrix)[0][1]*100
  MatchPercentage=round(MatchPercentage,2)
  #print('Match Percentage is :'+ str(MatchPercentage)+'% to Requirement')
  return MatchPercentage
  
def main():
  st.title("Resume Mapping")
  cv_files = st.file_uploader("Choose the cv files to be mapped ", accept_multiple_files=True)
  #option = st.selectbox('file type',('text','pdf'))
  
  #only one file for job description
  jd_file=st.file_uploader("Choose the job description file",accept_multiple_files=False) 
  jd_text=read_pdf_with_pdfplumber(jd_file)
  jd_clear=cleartext(jd_text)
  match_file=[]
  result = st.button("Get result")
  if result and uploaded_files is not None:
    for cv_file in cv_files:
      cv_text= read_pdf_with_pdfplumber(cv_file)
      cv_clear=cleartext(cv_text)
      Match=check_similarity(cv_clear, jd_clear)
      match_file.append({"File": cv_file,
                         "Match%": Match})
      df= pd.DataFrame(match_file)
      df=df.astype(str)
      df.to_feather('df')
    
  st.dataframe(df[["File", "Match%"]])   

  csv = df.to_csv().encode('utf-8')
  st.download_button(label="Download data as CSV",
                           data=csv,
                           file_name='cv_df.csv',
                           mime='text/csv',) 

if __name__ == "__main__":
  main()
  
  