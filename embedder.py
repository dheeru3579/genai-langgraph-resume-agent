import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

text = "Spring Boot is a Java framework used to build backend applications."

response = client.models.embed_content(
    model="gemini-embedding-001",
    contents=text
)

embedding = response.embeddings[0].values

print("Embedding length:", len(embedding))
print("First 10 values:", embedding[:10])