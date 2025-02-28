import pdfplumber

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

# pdf_path = r"c:\Users\akars\Downloads\akarshan_cv.pdf"

# resume_text = extract_text_from_pdf(pdf_path)
# print(resume_text)