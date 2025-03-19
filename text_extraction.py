import os
import json
import hashlib
import pytesseract
from pdf2image import convert_from_path

JSON_FILE = "extracted_data.json"

def generate_agreement_id(name):
    """Generate unique agreement ID using name + hash."""
    hash_part = hashlib.md5(name.encode()).hexdigest()[:8]  # First 8 chars of MD5 hash
    return f"AG_{name}_{hash_part}"


def save_extracted_text(agreement_id, text):
    """ Save extracted text persistently in json file """
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r') as f:
            extracted_data = json.load(f) # Load JSON file 
    else:
        extracted_data = {} # if JSON file not already exists
    extracted_data[agreement_id] = text #add/update the extracted text
    with open(JSON_FILE, 'w') as f:
        json.dump(extracted_data, f, indent=4)
    print(f"✅ Text saved for {agreement_id}")    


def get_extracted_text(agreement_id):
    """ Retrieve extracted text from JSON if available """
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r') as f:
            extracted_data = json.load(f)
        return extracted_data.get(agreement_id,None)
    return None


def read_pdf_ocr(pdf_path, agreement_id):
    """Extract text from a single PDF using OCR. But check JSON before processing"""
    existing_text = get_extracted_text(agreement_id) # calling function, if output exists => text exists
    if existing_text:
        print(f"✅ Using cached text for {agreement_id}")   
        return existing_text # If found, return file content  
    try:
        images = convert_from_path(pdf_path)
        text = "\n".join([pytesseract.image_to_string(image) for image in images]).strip()
        if text:
            save_extracted_text(agreement_id, text) # saves text to JSON for future use
            return text     
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return None 
    return None # Return none if ocr fails


def process_multiple_pdfs(folder_path):
    """Process multiple PDFs in a folder and save extracted text."""
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]
    if not pdf_files:
        print("No PDFs found in the provided folder.")
        return
    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        agreement_name, _ = os.path.splitext(pdf_file)  # Extract name without .pdf
        agreement_id = generate_agreement_id(agreement_name)
        
        extracted_text = read_pdf_ocr(pdf_path,agreement_id) # Save text to respective agreement id
        
        if extracted_text:
            print(f"✅ Successfully processed: {pdf_file}")
        else:
            print(f"⚠️ Skipping {pdf_file} due to extraction failure.")
