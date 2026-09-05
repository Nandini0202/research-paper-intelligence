from src.pdf_processor import extract_text_from_pdf, remove_repeated_headers, clean_text

pages = extract_text_from_pdf("data/sample_paper.pdf")
pages = remove_repeated_headers(pages)

print("Number of pages:", len(pages))

for page in pages:
    cleaned_text = clean_text(page["text"])

    print("\n--- Page", page["page"], "---")
    print(cleaned_text[:500])