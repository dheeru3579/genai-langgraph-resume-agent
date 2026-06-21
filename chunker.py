def chunk_text(text, chunk_size=500):
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)

    return chunks


sample_text = """
Spring Boot is a Java framework.
It simplifies backend development.
Dependency Injection is one of its core features.
"""

chunks = chunk_text(sample_text, 50)

for idx, chunk in enumerate(chunks):
    print(f"\nChunk {idx+1}")
    print(chunk)