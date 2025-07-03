import pandas as pd
import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_bytes
import io

def parse_document(file):
    # Streamlit UploadedFile uses .name, not .filename
    filename = file.name if hasattr(file, 'name') else file.filename
    if filename.endswith('.pdf'):
        return parse_pdf(file)
    elif filename.endswith('.xlsx'):
        return pd.read_excel(file)
    elif filename.endswith('.csv'):
        return pd.read_csv(file)
    else:
        raise ValueError("Unsupported file format")

def parse_pdf(file):
    images = convert_from_bytes(file.file.read())
    text_data = ""
    for image in images:
        text_data += pytesseract.image_to_string(image)
    return pd.read_csv(io.StringIO(text_data))