import fitz  # PyMuPDF
from collections import Counter

def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def calculate_ats_score(resume_text, job_description):
    resume_words = resume_text.lower().split()
    job_words = job_description.lower().split()

    resume_word_count = Counter(resume_words)
    job_word_count = Counter(job_words)

    matched = sum(min(resume_word_count[word], job_word_count[word]) for word in job_word_count)
    total = sum(job_word_count.values())

    score = (matched / total) * 100 if total > 0 else 0
    return round(score, 2)
