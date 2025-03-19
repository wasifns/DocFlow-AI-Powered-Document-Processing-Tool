import os
import json
import hashlib
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from config import agent  # Import the AI agent
from text_extraction import generate_agreement_id
JSON_FILE = "extracted_data.json"

def process_multiple_pdfs(folder_path):
    """ Processes multiple PDFs in a folder, extracts text, and saves it in JSON storage. """
    agreement_data = load_data() # Checks existing json data

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            agreement_id = generate_agreement_id(filename)

            if agreement_id in agreement_data:
                print(f"✅ Skipping {filename}, already extracted.")
                continue # Avoid reprocessing
            
            extracted_text = extract_text_from_pdf(pdf_path)
            if extracted_text:
                agreement_data[agreement_id] = extracted_text
                print(f"✅ Extracted text saved for {filename}")
                
    save_data(agreement_data)

def extract_text_from_pdf(pdf_path):
    """
    Converts PDF pages to images and extracts text using OCR.
    """
    images = convert_from_path(pdf_path)
    extracted_text = ""

    for img in images:
        extracted_text += pytesseract.image_to_string(img) + "\n"

    return extracted_text.strip()

def load_data():
    """Load extracted text form JSON storage"""
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            return json.load(f) # load and return Json data
    else:
        return {} # Return Empyt dict
    
def ask_question(agreements_data, agreement_id, query):
    """ Uses the AI agent to answer queries about a specific agreement."""
    if agreement_id not in agreements_data:
        return "Invalid Agreement ID. Try again."

    document_text = agreements_data[agreement_id]
    response = agent.run(f"Context: {document_text}\n\nQuestion: {query}")
    return response.content if response else "No response generated."

def save_data(data):
    """Save extracted text to JSON storage"""
    with open(JSON_FILE,'w', encoding = "utf-8") as f:
        json.dump(data, f, indent=4) # Save updated json data