import chromadb
from sentence_transformers import SentenceTransformer

CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "gmu_student_survival_guide"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
N_RESULTS = 5


def retrieve(query, n_results=N_RESULTS):
    model = SentenceTransformer(EMBEDDING_MODEL)

    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_collection(name=COLLECTION_NAME)

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )

    retrieved_chunks = []

    for text, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        retrieved_chunks.append(
            {
                "text": text,
                "source": metadata["source"],
                "distance": distance,
            }
        )

    return retrieved_chunks


if __name__ == "__main__":
    test_query = "What advice do GMU students give incoming freshmen?"
    results = retrieve(test_query)

    print(f"Query: {test_query}\n")

    for i, result in enumerate(results, start=1):
        print(f"Result {i}")
        print(f"Source: {result['source']}")
        print(f"Distance: {result['distance']}")
        print(result["text"][:400])
        print("-" * 50)