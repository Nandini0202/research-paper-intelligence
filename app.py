from src.embeddings import create_embeddings, model
from src.retrieval import search_faiss
from src.vector_store import create_faiss_index

from src.pdf_processor import (
    extract_text_from_pdf,
    remove_repeated_headers,
    clean_text,
    create_chunks
)

pages = extract_text_from_pdf("data/sample_paper.pdf")

pages = remove_repeated_headers(pages)

for page in pages:
    page["text"] = clean_text(page["text"])

chunks = create_chunks(pages)
embeddings = create_embeddings(chunks)
index = create_faiss_index(embeddings)

print("FAISS index size:", index.ntotal)
query = "What methodology did the researchers use?"

results = search_faiss(
    query,
    chunks,
    index,
    model,
    top_k=3
)

print("\n===== SEARCH RESULTS =====")

for result in results:
    print(
        f"\nChunk: {result['chunk_id']}"
        f" | Page: {result['page']}"
        f" | Score: {result['score']:.4f}"
    )
    print(result["text"][:500])

print("Number of pages:", len(pages))
print("Number of chunks:", len(chunks))
print("Embedding shape:", embeddings.shape)

for chunk in chunks[:5]:
    print(
    "\n--- Chunk", chunk["chunk_id"],
    "| Page", chunk["page"], "---"
)
    print(chunk["text"][:300])