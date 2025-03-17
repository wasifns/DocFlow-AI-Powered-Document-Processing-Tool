from agno.agent import Agent
from agno.models.google import Gemini
from dotenv import load_dotenv
from pdf2image import convert_from_path  
import pytesseract
from PIL import Image
import os

load_dotenv()

# Function to extract text from a PDF using OCR
def read_pdf_ocr(pdf_path):
    try:
        images = convert_from_path(pdf_path)  # Convert PDF pages to images
        text = ""
        for image in images:
            text += pytesseract.image_to_string(image) + "\n"
        return text
    except Exception as e:
        print(f"Error reading PDF with OCR: {e}")
        return None

# Process single or multiple PDFs
def process_pdfs():
    choice = input("Do you want to process a single (S) or multiple (M) agreements? ").strip().lower()
    
    if choice == "s":
        pdf_file = input("Enter full path of the PDF file:\n").strip()
        pdf_content = read_pdf_ocr(pdf_file)
        files = [pdf_file]  # Store in list to handle uniformly
    
    elif choice == "m":
        folder_path = input("Enter the folder path containing PDFs:\n").strip()
        files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".pdf")]
        pdf_content = "\n\n".join([read_pdf_ocr(file) for file in files])  # Merge text from all PDFs
    
    else:
        print("Invalid choice. Exiting.")
        return
    
    if not pdf_content:
        print("Could not load any PDF content. Exiting.")
        return
    
    return pdf_content, files

# Agent setup
model_id = "gemini-1.5-flash"
agent = Agent(
    model=Gemini(id=model_id),
    markdown=True,
)

pdf_content, files = process_pdfs()
if not pdf_content:
    exit()

print(f"Loaded {len(files)} document(s).\nAsk questions about the content. Type 'exit' to quit.")

while True:
    question = input("You: ")
    if question.lower() == "exit":
        break

    try:
        prompt = f"Given the following PDF content:\n\n{pdf_content}\n\nQuestion: {question}"
        response = agent.print_response(prompt)
        print("Agent:", response)
    except Exception as e:
        print(f"Error: {e}")

print("Bye!")
