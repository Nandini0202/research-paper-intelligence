from src.pdf_processor import extract_text_from_pdf

pages = extract_text_from_pdf("data/sample_paper.pdf")

print("Number of pages:", len(pages))

for page in pages:
    print("\n--- Page", page["page"], "---")
    print(page["text"][:500])