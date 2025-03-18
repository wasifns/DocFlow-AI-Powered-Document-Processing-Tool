import os
import json
import hashlib
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from config import agent  # Import the AI agent

def process_multiple_pdfs(folder_path, extracted_text_folder):
    """
    Processes multiple PDFs in a folder, extracts text, and saves it as .txt files.
    """
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            extracted_text = extract_text_from_pdf(pdf_path)

            # Create a unique filename using a hash
            file_hash = hashlib.md5(pdf_path.encode()).hexdigest()[:8]
            text_filename = f"AG_{filename.replace('.pdf', '')}_{file_hash}.txt"
            text_file_path = os.path.join(extracted_text_folder, text_filename)

            with open(text_file_path, "w", encoding="utf-8") as f:
                f.write(extracted_text)

            print(f"Extracted text saved: {text_file_path}")

def extract_text_from_pdf(pdf_path):
    """
    Converts PDF pages to images and extracts text using OCR.
    """
    images = convert_from_path(pdf_path)
    extracted_text = ""

    for img in images:
        extracted_text += pytesseract.image_to_string(img) + "\n"

    return extracted_text.strip()

def load_extracted_text(extracted_text_folder):
    """
    Loads extracted text from the folder into a dictionary.
    """
    agreements_data = {}

    for filename in os.listdir(extracted_text_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(extracted_text_folder, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                agreements_data[filename] = f.read()

    return agreements_data

def ask_question(agreements_data, agreement_id, query):
    """
    Uses the AI agent to answer queries about a specific agreement.
    """
    if agreement_id not in agreements_data:
        return "Invalid Agreement ID. Try again."

    document_text = agreements_data[agreement_id]
    response = agent.run(f"Context: {document_text}\n\nQuestion: {query}")
    # print(response)  # Debugging: See what response contains
    # print(dir(response))  # See available attributes and methods

    return response.content if response else "No response generated."
