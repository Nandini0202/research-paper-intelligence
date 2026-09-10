import numpy as np


def search_faiss(query, chunks, index, model, top_k=3):
    # Convert the question into an embedding
    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    )

    query_embedding = np.asarray(
        query_embedding,
        dtype="float32"
    )

    # Search the FAISS index
    scores, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for score, index_position in zip(scores[0], indices[0]):
        results.append({
            "chunk_id": chunks[index_position]["chunk_id"],
            "page": chunks[index_position]["page"],
            "score": float(score),
            "text": chunks[index_position]["text"]
        })

    return results