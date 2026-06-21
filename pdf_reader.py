from pypdf import PdfReader

reader = PdfReader("data/sample.pdf")

text = ""

for page in reader.pages:
    text += page.extract_text()

print(text)