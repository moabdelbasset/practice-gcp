from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image
import streamlit as st

st.title("PDF MCQ Extractor")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    pages = convert_from_bytes(uploaded_file.read())

    for i, page in enumerate(pages):
        st.subheader(f"Page {i + 1}")
        st.image(page, use_column_width=True)
        text = pytesseract.image_to_string(page)
        st.text_area("Extracted Text", text, height=200)
