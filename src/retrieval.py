import numpy as np


def search_similar_chunks(query, chunks, embeddings, model, top_k=3):
    # Convert the user's question into an embedding
    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    )[0]

    # Calculate similarity with every chunk
    scores = np.dot(embeddings, query_embedding)

    # Get indices of highest scores
    top_indices = np.argsort(scores)[::-1][:top_k]

    results = []

    for index in top_indices:
        results.append({
            "chunk_id": chunks[index]["chunk_id"],
            "page": chunks[index]["page"],
            "score": float(scores[index]),
            "text": chunks[index]["text"]
        })

    return results