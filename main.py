import os
from config import agent  # Import the AI agent from config.py
from utils import process_multiple_pdfs, load_data, ask_question, save_data


# Get folder path from user
folder_path = input("Enter the folder path containing agreements:\n").strip()


if os.path.isdir(folder_path):
    JSON_FILE = os.path.join(folder_path,"extracted_data.json")
    
    # Process PDFs and extract text
    process_multiple_pdfs(folder_path, JSON_FILE)
    
    # Load extracted data
    agreements_data = load_data(JSON_FILE)
    
    if not agreements_data:
        print("No agreements found. Exiting.")
        exit()

    # Querying loop
    last_agreement_id = None
    while True:
        if last_agreement_id:
            agreement_id = input(f"Press Enter to use {last_agreement_id} or New Enter Agreement ID to query (or type 'exit' to quit): ").strip()
        else:
            agreement_id = input("Enter Agreement ID to query (or type 'exit' to quit): ").strip()
        if agreement_id.lower() == "exit":
            break
        elif agreement_id:
            last_agreement_id = agreement_id

        if not last_agreement_id:
            print("No Agreement ID selected. Please enter an ID.")
            continue  # Ask again if no ID is available
        
        query = input("Ask a question about the agreement:\n").strip()
        response = ask_question(agreements_data, last_agreement_id, query)   
        print("\nResponse:\n", response)

else:
    print("Invalid folder path. Please check and try again.")
