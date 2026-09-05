import re
from pypdf import PdfReader
from collections import Counter


def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        pages.append({
            "page": page_number,
            "text": text
        })

    return pages

def remove_repeated_headers(pages):
    first_lines = []

    for page in pages[1:]:
        lines = page["text"].splitlines()

        if lines:
            first_lines.append(lines[0].strip())

    counts = Counter(first_lines)

    repeated_headers = {
        line
        for line, count in counts.items()
        if count >= 3 and len(line) < 80
    }

    for page in pages:
        lines = page["text"].splitlines()

        if lines and lines[0].strip() in repeated_headers:
            lines = lines[1:]

        page["text"] = "\n".join(lines)

    return pages



def clean_text(text):
    text = text.replace("-\n", "")
    text = re.sub(r"\s+", " ", text)

    return text.strip()