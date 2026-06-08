from pathlib import Path

DOCUMENTS_DIR = "documents"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150


def load_documents():
    docs = []

    for file_path in Path(DOCUMENTS_DIR).glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")

        docs.append(
            {
                "source": file_path.name,
                "text": text
            }
        )

    return docs


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def chunk_documents(documents):
    all_chunks = []

    for doc in documents:
        chunks = chunk_text(doc["text"])

        for i, chunk in enumerate(chunks):
            all_chunks.append(
                {
                    "id": f"{doc['source']}_chunk_{i}",
                    "source": doc["source"],
                    "chunk_index": i,
                    "text": chunk
                }
            )

    return all_chunks


if __name__ == "__main__":
    documents = load_documents()
    chunks = chunk_documents(documents)

    print(f"Loaded {len(documents)} documents.")
    print(f"Created {len(chunks)} chunks.\n")

    print("Sample chunk:")
    print("-" * 50)
    print(chunks[0]["text"])
    print("-" * 50)
    print(f"Source: {chunks[0]['source']}")