import chromadb
from sentence_transformers import SentenceTransformer

from ingest import load_documents, chunk_documents

CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "gmu_student_survival_guide"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def build_index():
    documents = load_documents()
    chunks = chunk_documents(documents)

    print(f"Loaded {len(documents)} documents.")
    print(f"Created {len(chunks)} chunks.")
    print("Loading embedding model...")

    model = SentenceTransformer(EMBEDDING_MODEL)

    texts = [chunk["text"] for chunk in chunks]
    ids = [chunk["id"] for chunk in chunks]
    metadatas = [
        {
            "source": chunk["source"],
            "chunk_index": chunk["chunk_index"],
        }
        for chunk in chunks
    ]

    print("Creating embeddings...")
    embeddings = model.encode(texts).tolist()

    print("Saving embeddings to ChromaDB...")
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(name=COLLECTION_NAME)

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(f"Saved {collection.count()} chunks to ChromaDB.")


if __name__ == "__main__":
    build_index()