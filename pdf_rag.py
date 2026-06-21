import os
from dotenv import load_dotenv
import chromadb
from pypdf import PdfReader
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text

def chunk_text(text, chunk_size=700):
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)

    return chunks

pdf_text = read_pdf("data/sample.pdf")
chunks = chunk_text(pdf_text)

client = chromadb.Client()
collection = client.create_collection(name="pdf_rag_collection")

for index, chunk in enumerate(chunks):
    collection.add(
        documents=[chunk],
        ids=[f"chunk_{index}"]
    )

question = input("Ask a question from your PDF: ")

results = collection.query(
    query_texts=[question],
    n_results=3
)

retrieved_chunks = results["documents"][0]

context = "\n\n".join(retrieved_chunks)

prompt = f"""
You are a helpful assistant.
Answer the question using only the context below.
If the answer is not in the context, say: "I don't know based on the PDF."

Context:
{context}

Question:
{question}
"""

model = genai.GenerativeModel("gemini-2.5-flash")
response = model.generate_content(prompt)

print("\nAnswer:")
print(response.text)