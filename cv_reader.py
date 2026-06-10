from pypdf import PdfReader

def extract_cv_text(pdf_path="cv.pdf"):
    reader = PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text
    return full_text
