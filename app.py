import streamlit as st
from pdf2image import convert_from_bytes
import pytesseract
import cv2
import numpy as np
from PIL import Image

st.set_page_config(layout="wide")
st.title("📘 MCQ Practice from PDF")

uploaded_file = st.file_uploader("Upload PDF with MCQs", type=["pdf"])

def extract_highlighted_text(img_pil):
    # Convert to OpenCV image and HSV
    img_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)

    # Define yellow highlight range
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])

    # Create mask for yellow areas
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    result = cv2.bitwise_and(img_cv, img_cv, mask=mask)

    # Convert result to PIL and run OCR
    result_pil = Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    highlighted_text = pytesseract.image_to_string(result_pil)

    return highlighted_text.strip()

if uploaded_file:
    st.success("PDF uploaded!")
    pages = convert_from_bytes(uploaded_file.read())

    questions = []

    for i, page in enumerate(pages):
        st.subheader(f"📄 Page {i+1}")
        st.image(page, use_column_width=True)

        # Extract full OCR text
        text = pytesseract.image_to_string(page)
        st.text_area("📄 OCR Text", text, height=150)

        # Extract highlighted text (attempt)
        highlighted = extract_highlighted_text(page)
        st.text_area("✨ Detected Highlighted Answer", highlighted, height=100)

        questions.append({
            "page": i + 1,
            "ocr_text": text,
            "highlight": highlighted
        })

    st.success("All pages processed!")
