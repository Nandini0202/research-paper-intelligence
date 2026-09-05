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
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n+", "\n", text)

    return text.strip()


def create_chunks(pages, chunk_size=1000, overlap=200):
    chunks = []
    chunk_id = 1

    for page in pages:
        text = re.sub(r"\s+", " ", page["text"]).strip()

        sentences = re.split(r"(?<=[.!?])\s+", text)

        current_chunk = ""

        for sentence in sentences:
            sentence = sentence.strip()

            if not sentence:
                continue

            # Normal case: sentence fits in the chunk
            if len(current_chunk) + len(sentence) + 1 <= chunk_size:
                current_chunk += sentence + " "

            else:
                # Save existing chunk
                if current_chunk.strip():
                    chunks.append({
                        "chunk_id": chunk_id,
                        "page": page["page"],
                        "text": current_chunk.strip()
                    })

                    chunk_id += 1

                # Keep overlap from previous chunk
                overlap_words = current_chunk.split()[-40:]
                overlap_text = " ".join(overlap_words)

                current_chunk = overlap_text + " " + sentence

                # If the sentence itself is too long,
                # split it at word boundaries
                while len(current_chunk) > chunk_size:
                    words = current_chunk.split()
                    part = ""

                    for word in words:
                        if len(part) + len(word) + 1 <= chunk_size:
                            part += word + " "
                        else:
                            break

                    if not part:
                        break

                    chunks.append({
                        "chunk_id": chunk_id,
                        "page": page["page"],
                        "text": part.strip()
                    })

                    chunk_id += 1

                    remaining = current_chunk[len(part):].strip()
                    current_chunk = remaining

        if current_chunk.strip():
            chunks.append({
                "chunk_id": chunk_id,
                "page": page["page"],
                "text": current_chunk.strip()
            })

            chunk_id += 1

    return chunks