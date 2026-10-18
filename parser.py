# parser.py
import re
import pdfplumber
import docx

def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    return text

def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def analyze_resume(resume_text, role_data):
    clean_text = resume_text.lower()
    results = {}
    total_keywords = 0
    total_matched = 0

    for category, keywords in role_data.items():
        found = []
        missing = []
        for kw in keywords:
            total_keywords += 1
            # Use regex word boundaries for accurate keyword matching
            pattern = r'\b' + re.escape(kw.lower()) + r'\b'
            if re.search(pattern, clean_text):
                found.append(kw.title())
                total_matched += 1
            else:
                missing.append(kw.title())
        results[category] = {"found": found, "missing": missing}

    score = int((total_matched / total_keywords) * 100) if total_keywords > 0 else 0
    return score, results