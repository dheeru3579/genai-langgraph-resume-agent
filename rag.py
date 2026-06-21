import os
from dotenv import load_dotenv
import chromadb
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

client = chromadb.Client()

collection = client.create_collection(name="genai_rag")

collection.add(
    documents=[
        "Spring Boot is a Java framework used to build backend applications.",
        "React is a JavaScript library used to build user interfaces.",
        "ChromaDB is a vector database used to store embeddings."
    ],
    ids=["doc1", "doc2", "doc3"]
)

question = "What is used for backend development in Java?"

results = collection.query(
    query_texts=[question],
    n_results=1
)

context = results["documents"][0][0]

prompt = f"""
Answer the question using only the context below.

Context:
{context}

Question:
{question}
"""

model = genai.GenerativeModel("gemini-2.5-flash")

response = model.generate_content(prompt)

print(response.text)