import fitz  # PyMuPDF
import docx
import pandas as pd
import os

def extract_text_from_pdf(file_path):
    text = ""
    try:
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text() + "\n\n"
        doc.close()
    except Exception as e:
        print(f"Error parsing PDF: {e}")
    return text.strip()

def extract_text_from_docx(file_path):
    text = ""
    try:
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Error parsing DOCX: {e}")
    return text.strip()

def extract_text_from_excel(file_path):
    text = ""
    try:
        df_dict = pd.read_excel(file_path, sheet_name=None)
        for sheet_name, df in df_dict.items():
            text += f"--- Sheet: {sheet_name} ---\n"
            text += df.to_csv(index=False) + "\n\n"
    except Exception as e:
        print(f"Error parsing Excel: {e}")
    return text.strip()

def extract_text_from_txt(file_path):
    text = ""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        print(f"Error parsing TXT: {e}")
    return text.strip()

def extract_text(file_path, file_type):
    ext = file_type.lower()
    if ext == 'pdf':
        return extract_text_from_pdf(file_path)
    elif ext == 'docx':
        return extract_text_from_docx(file_path)
    elif ext in ['xlsx', 'xls']:
        return extract_text_from_excel(file_path)
    elif ext == 'txt':
        return extract_text_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start += (chunk_size - overlap)
    return chunks
