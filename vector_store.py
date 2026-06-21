import chromadb

client = chromadb.Client()

collection = client.create_collection(name="genai_notes")

collection.add(
    documents=[
        "Spring Boot is a Java framework used to build backend applications.",
        "React is a JavaScript library used to build user interfaces.",
        "ChromaDB is a vector database used to store embeddings."
    ],
    ids=["doc1", "doc2", "doc3"]
)

results = collection.query(
    query_texts=["What is used for backend development in Java?"],
    n_results=2
)

print(results)