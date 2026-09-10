from src.embeddings import create_embeddings

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

print("Number of pages:", len(pages))
print("Number of chunks:", len(chunks))
print("Embedding shape:", embeddings.shape)

for chunk in chunks[:5]:
    print(
    "\n--- Chunk", chunk["chunk_id"],
    "| Page", chunk["page"], "---"
)
    print(chunk["text"][:300])