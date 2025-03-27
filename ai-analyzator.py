import cv2
import pytesseract
import numpy as np
import streamlit as st
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'D:\tesseract\tesseract.exe'  

def process_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY)
    return thresh

def assess_readability(text):
    if not text:
        return 1  
    
    length_score = min(len(text) / 100, 1)  
    noise_score = text.count("!") + text.count("?")  
    noise_score = min(noise_score / 10, 1)  
    
    score = 10 * (1 - noise_score) * length_score
    return round(score)

#Streamlit-интерфейс
st.title("AI-анализатор текста с фото")

uploaded_file = st.file_uploader("Выберите фото с текстом", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Загруженное изображение", use_column_width=True)
    
    img_cv = np.array(image)
    
    processed_img = process_image(img_cv)
    
    text = pytesseract.image_to_string(processed_img)
    st.text_area("Распознанный текст", text)
    
    readability_score = assess_readability(text)
    st.write(f"Читаемость текста: {readability_score}/10")
