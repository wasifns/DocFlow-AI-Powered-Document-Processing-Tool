import re

def extract_information(agreement_text, query):
    """Extract specific information from an agreement text using keyword lookup."""
    patterns = {
        "due amount": r"\$\d+(?:,\d{3})*(?:\.\d{2})?",  # Matches amounts like $1,000.00
        "due date": r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}\b",  # Matches "January 25, 2025"
        "company name": r"Company\s+[A-Za-z]+"  # Matches "Company A"
    }
    
    for key, pattern in patterns.items():
        if key in query.lower():
            matches = re.findall(pattern, agreement_text)
            return matches[0] if matches else f"{key.capitalize()} not found."
    
    return "I'm not sure. Try rephrasing your question."

def ask_question(agreements_data, agreement_id, query):
    """Answer questions based on extracted text of a specific agreement."""
    if agreement_id not in agreements_data:
        return "Agreement ID not found."
    
    agreement_text = agreements_data[agreement_id]
    return extract_information(agreement_text, query)
