import cv2
import pytesseract
import numpy as np
import streamlit as st
from PIL import Image

# Убедись, что путь к tesseract правильный
pytesseract.pytesseract.tesseract_cmd = r'D:\tesseract\tesseract.exe'  # укажи свой путь

# Функция для обработки изображения
def process_image(image):
    # Конвертируем изображение в оттенки серого
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Применяем гауссово размытие для уменьшения шума
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # Используем пороговую фильтрацию для улучшения контраста
    _, thresh = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY)
    return thresh

# Функция для оценки читаемости
def assess_readability(text):
    if not text:
        return 1  # Если текста нет, то оцениваем как 1 (нечитабельно)
    
    # Простейшая метрика: если длина текста маленькая или в нем много спецсимволов, то плохо
    length_score = min(len(text) / 100, 1)  # Чем больше текста, тем лучше (макс. 1)
    noise_score = text.count("!") + text.count("?")  # Много знаков препинания = хуже читаемость
    noise_score = min(noise_score / 10, 1)  # Считаем шум как отношение к 10
    
    # Возвращаем оценку от 1 до 10
    score = 10 * (1 - noise_score) * length_score
    return round(score)

# Streamlit интерфейс
st.title("AI-анализатор текста с фото")

uploaded_file = st.file_uploader("Выберите фото с текстом", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Загружаем и показываем изображение
    image = Image.open(uploaded_file)
    st.image(image, caption="Загруженное изображение", use_column_width=True)
    
    # Преобразуем изображение в массив OpenCV
    img_cv = np.array(image)
    
    # Обрабатываем изображение
    processed_img = process_image(img_cv)
    
    # Распознаем текст
    text = pytesseract.image_to_string(processed_img)
    st.text_area("Распознанный текст", text)
    
    # Оцениваем читаемость
    readability_score = assess_readability(text)
    st.write(f"Читаемость текста: {readability_score}/10")
