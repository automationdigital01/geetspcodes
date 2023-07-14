import cv2
from pytesseract import Output
import streamlit as st
from PIL import Image
#load image
st.title("Text Extract")
image= st.uploader("Choose a file")
st.image(image, caption= "loaded image")

#giving options to extract whole text content or particular text
with col1:
    option= st.radio("How you want the output, please choose from below :",
             key="visibility",
             options= ["Extract whole text","Extract partcular text"])
    
if option=="Extract partcular text":
    text=st.text_input("text to be searched", "")
    d = pytesseract.image_to_data(img, output_type=Output.DICT)
    keys = list(d.keys())
    n_boxes = len(d['text'])
    for i in range(n_boxes):
        if float(d['conf'][i]) > 60:
            if re.match(data_pattern, d['text'][i]):
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
Image.fromarray(img)
