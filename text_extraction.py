import os
import hashlib
import pytesseract
from pdf2image import convert_from_path

def generate_agreement_id(name):
    """Generate unique agreement ID using name + hash."""
    hash_part = hashlib.md5(name.encode()).hexdigest()[:8]  # First 8 chars of MD5 hash
    return f"AG_{name}_{hash_part}"

def read_pdf_ocr(pdf_path):
    """Extract text from a single PDF using OCR."""
    try:
        images = convert_from_path(pdf_path)
        text = "\n".join([pytesseract.image_to_string(image) for image in images])
        return text.strip()
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return None

def process_multiple_pdfs(folder_path, extracted_text_folder):
    """Process multiple PDFs in a folder and save extracted text."""
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]

    if not pdf_files:
        print("No PDFs found in the provided folder.")
        return

    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        agreement_name, _ = os.path.splitext(pdf_file)  # Extract name without .pdf
        agreement_id = generate_agreement_id(agreement_name)
        
        extracted_text = read_pdf_ocr(pdf_path)
        
        if extracted_text:
            file_name = f"{agreement_id}.txt"
            file_path = os.path.join(extracted_text_folder, file_name)
            
            with open(file_path, "w", encoding="utf-8") as text_file:
                text_file.write(extracted_text)

            print(f"Extracted text saved: {file_path}")
        else:
            print(f"Skipping {pdf_file} due to extraction failure.")
