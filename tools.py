from pypdf import PdfReader


def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


def save_report(content, file_name="resume_analysis_report.txt"):
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(content)

    return f"Report saved successfully as {file_name}"

def read_text_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()