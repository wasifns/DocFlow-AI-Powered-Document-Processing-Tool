from agno.agent import Agent
from agno.models.google import Gemini
from dotenv import load_dotenv
from pdf2image import convert_from_path  
import pytesseract
from PIL import Image
import os
import hashlib
import re

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

def create_folder(base_path):
    """Ask user to name a folder and create it in the provided directory."""
    while True:
        folder_name = input("Enter the name for the extracted-text folder:\n").strip()
        new_folder_path = os.path.join(base_path, folder_name)
        
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)
            return new_folder_path  # Return the newly created folder path
        else:
            print("Folder already exists! Choose a different name.")

def process_multiple_pdfs(folder_path):
    """Process multiple PDFs in a folder and save extracted text to user-defined folder."""
    # Ask user for extracted-text folder name and create it
    extracted_text_folder = create_folder(folder_path)

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

def load_extracted_text(folder_path):
    """Load extracted agreement text from all .txt files in the folder."""
    agreements_data = {}  # Dictionary to store {agreement_id: text}
    
    for file in os.listdir(folder_path):
        if file.endswith(".txt"):
            agreement_id = file.replace(".txt", "")  # Extract ID from filename
            with open(os.path.join(folder_path, file), "r", encoding="utf-8") as f:
                agreements_data[agreement_id] = f.read()
    
    return agreements_data  # Returns a dictionary of agreements

def extract_information(agreement_text, query):
    """Extract specific information from an agreement text using keyword lookup and regex."""
    patterns = {
        "due amount": r"\b(?:USD|\$)?\s?(\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)\b",  # Matches $1,000.00 or 1000
        "due date": r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}\b",  # Matches "January 25, 2025"
        "company name": r"Company\s+([A-Z][a-zA-Z]+)"  # Matches "Company A"
    }
    
    extracted_data = {}
    
    for key, pattern in patterns.items():
        matches = re.findall(pattern, agreement_text)
        extracted_data[key] = matches[0] if matches else None
    
    # Return a structured response
    if extracted_data["company name"] and extracted_data["due amount"] and extracted_data["due date"]:
        return f"{extracted_data['company name']} owes you ${extracted_data['due amount']} due on {extracted_data['due date']}."
    
    return "Information not found. Try rephrasing your question."

def ask_question(agreements_data, agreement_id, query):
    """Retrieve structured answer based on agreement text."""
    if agreement_id not in agreements_data:
        return "Agreement ID not found. Please check the ID and try again."
    
    agreement_text = agreements_data[agreement_id]
    return extract_information(agreement_text, query)

# Main execution
# Process PDFs and extract text
folder_path = input("Enter the folder path containing agreements:\n").strip()
if os.path.isdir(folder_path):
    extracted_text_folder = create_folder(folder_path)  # Ensure the folder is created
    process_multiple_pdfs(folder_path)
    agreements_data = load_extracted_text(extracted_text_folder)  # Load extracted text
    print(agreements_data)
    while True:
        agreement_id = input("\nEnter Agreement ID to query (or type 'exit' to quit): ").strip()
        if agreement_id.lower() == "exit":
            break
        if agreement_id not in agreements_data:
            print("Invalid Agreement ID. Try again.")
            continue
        query = input("Enter your question about the agreement: ").strip()
        answer = ask_question(agreements_data, agreement_id, query)
        print("\nAnswer:", answer)

else:
    print("Invalid folder path. Please check and try again.")
    exit()

