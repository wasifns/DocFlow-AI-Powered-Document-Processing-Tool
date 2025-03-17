from agno.agent import Agent
from agno.models.google import Gemini
from dotenv import load_dotenv
import os
import pytesseract
from PIL import Image
from pdf2image import convert_from_path  # added pdf2image

load_dotenv()

# PDF reading function using OCR
def read_pdf_ocr(pdf_path):
    try:
        images = convert_from_path(pdf_path)  # convert pdf to images.
        text = ""
        for image in images:
            text += pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Error reading PDF with OCR: {e}")
        return None

# Load PDF content
# pdf_file = "C:\\Mywork\\genAI-testing\\assets\\Wasif Ahmed (1).pdf"
# pdf_content = read_pdf_ocr(pdf_file)  # Use OCR function
pdf_file = input("Enter full path of the file\n")
pdf_content = read_pdf_ocr(pdf_file)

if not pdf_content:
    print("Could not load PDF content. Exiting.")
    exit()

# Agent setup
model_id = "gemini-2.0-flash"
agent = Agent(
    model=Gemini(id=model_id),
    markdown=True,
)

print(f"PDF '{pdf_file}' loaded.\nAsk questions about it. Type 'exit' to quit.")

while True:
    question = input("You: ")
    if question.lower() == "exit":
        break

    try:
        # Prepend PDF content to the question to provide context
        prompt = f"Given the following PDF content:\n\n{pdf_content}\n\nQuestion: {question}"
        response = agent.print_response(prompt)
        print("Agent:", response)
    except Exception as e:
        print(f"Error: {e}")

print("Bye!")


