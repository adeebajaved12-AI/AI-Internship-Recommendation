import fitz

def extract_text_from_pdf(pdf_path):
    text = ""
    # 'with' use karne se file automatic close ho jati hai
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text.lower()

def extract_skills(text):
    # Updated skill database based on your actual CV
    skill_db = [
        "python", "c++", "sql", "tensorflow", "scikit-learn", "flask", 
        "machine learning", "deep learning", "nlp", "computer vision", 
        "lstm", "database management", "css", "java"
    ]
    found_skills = [skill for skill in skill_db if skill in text.lower()]
    return list(set(found_skills))