import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
import docx2txt
import pdfplumber
import pickle
# import pytesseract 
# pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'
# config = ('-l eng --oem 1 --psm 3')
# importing the module
import wikipedia as wk
# import cv2

dep=["Depression is a mental state of low mood and aversion to activity.[2] Classified medically as a mental and behavioral disorder,[3] the experience of depression affects a person's thoughts, behavior, motivation, feelings, and sense of well-being.[4] The core symptom of depression is said to be anhedonia, which refers to loss of interest or a loss of feeling of pleasure in certain activities that usually bring joy to people."]
def result(text):
    res = wk.summary(text, sentences = 2)
    # printing the result
    return res

# def image_processing(img):
#     img2 = np.array(img)
#     norm_img = np.zeros((img2.shape[0], img2.shape[1]))
#     img2 = cv2.normalize(img2, norm_img, 0, 255, cv2.NORM_MINMAX)
#     img2 = cv2.threshold(img2, 100, 255, cv2.THRESH_BINARY)[1]
#     img2 = cv2.GaussianBlur(img2, (1, 1), 0)
#     text = pytesseract.image_to_string(img2, config=config)
#     return text


lst=["The text Starts here:"]

vectorizer = pickle.load(open('model (2).pkl', 'rb'))
model = pickle.load(open('vectorizer.pkl', 'rb'))

st.sidebar.title("Report Analyzer")

menu = ["DocumentFiles"]
choice = st.sidebar.selectbox("Menu",menu)


# def load_image(image_file):
#     img = Image.open(image_file)
#     return img

if choice == "Image":
    st.sidebar.subheader("Image")
    image_file = st.sidebar.file_uploader("Upload Images", type=["png","jpg","jpeg"])

    if image_file is not None:
        # Checking the details of File
        file_details = {"filename":image_file.name,"filetype":image_file.type,"filesize":image_file.size}
        st.write(file_details)
        img = load_image(image_file)
        text_res = image_processing(img)
        lst[0]+=text_res
        transformed_text = model.transform(lst)
        pred1 = vectorizer.predict(transformed_text)
        st.header(pred1[0])
        if(pred1[0]=="Depression"):
            st.write(dep[0])
            st.image(img, width=250)
        else:
            info = result(str(pred1[0]))
            st.write(info)
            st.image(img, width=250)
    
elif choice == "DocumentFiles":
    st.sidebar.subheader("DocumentFiles")
    docx_file = st.sidebar.file_uploader("Upload Document", type=["pdf","docx"])

    if st.sidebar.button("Process"):
        if docx_file is not None:
            file_details = {"filename":docx_file.name, "filetype":docx_file.type,
                                "filesize":docx_file.size}
            st.write(file_details)

            if docx_file.type == "text/plain":
    			# Read as string (decode bytes to string)
                raw_text = str(docx_file.read(),"utf-8")
                lst[0]+=raw_text
                transformed_text = model.transform(lst)
                pred1 = vectorizer.predict(transformed_text)
                st.header(pred1[0])
                st.text("Antidepressant")
                st.text("HyperTension")
                st.text("Disorder")

                if(pred1[0]=="Depression"):
                    st.write(dep[0])
                else:
                    info = result(str(pred1[0]))
                    st.write(info)
            
            elif docx_file.type == "application/pdf":
                try:
                    with pdfplumber.open(docx_file) as pdf:
                        pages = pdf.pages[0]
                        text = pages.extract_text()
                        lst[0]+=text
                        transformed_text = model.transform(lst)
                        pred1 = vectorizer.predict(transformed_text)
                        st.header(pred1[0])
                        if(pred1[0]=="Depression"):
                            st.write(dep[0])
                        else:
                            info = result(str(pred1[0]))
                            st.write(info)
                except:
                    st.write("None")
            else:
                raw_text = docx2txt.process(docx_file)
                st.write(raw_text)


            

