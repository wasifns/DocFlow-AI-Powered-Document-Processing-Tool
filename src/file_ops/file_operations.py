import os

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

def load_extracted_text(folder_path):
    """Load extracted agreement text from all .txt files in the folder."""
    agreements_data = {}

    if not os.path.exists(folder_path):
        print("Error: Folder does not exist!", folder_path)
        return agreements_data

    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if file.endswith(".txt") and os.path.isfile(file_path):
            agreement_id = file.replace(".txt", "")  # Extract ID from filename
            with open(file_path, "r", encoding="utf-8") as f:
                agreements_data[agreement_id] = f.read()
    
    return agreements_data
