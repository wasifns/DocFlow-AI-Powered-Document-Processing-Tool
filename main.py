import os
from config import agent  # Import the AI agent from config.py
from utils import process_multiple_pdfs, load_extracted_text, ask_question

# Get folder path from user
folder_path = input("Enter the folder path containing agreements:\n").strip()

if os.path.isdir(folder_path):
    extracted_text_folder = os.path.join(folder_path, "extracted_text")  # Fixed folder name
    os.makedirs(extracted_text_folder, exist_ok=True)  # Ensure it exists
    
    # Process PDFs and extract text
    process_multiple_pdfs(folder_path, extracted_text_folder)
    
    # Load extracted data
    agreements_data = load_extracted_text(extracted_text_folder)
    # print("Loaded Agreements Data:", agreements_data)  # Debugging

    
    if not agreements_data:
        print("No agreements found. Exiting.")
        exit()

    # Querying loop
    while True:
        agreement_id = input("Enter Agreement ID to query (or type 'exit' to quit): ").strip()
        if agreement_id.lower() == "exit":
            break
        
        query = input("Ask a question about the agreement:\n").strip()
        
        response = ask_question(agreements_data, agreement_id, query)
        
        print("\nResponse:\n", response)

else:
    print("Invalid folder path. Please check and try again.")
