from pypdf import PdfReader

PDF_PATH = "/Users/abdulsamadgilal/Development/Vector-Search-Engine/Vector-Search-Engine/pdf/gmail.pdf"

def load_pdf(file_path):
    reader = PdfReader(file_path)
    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            pages.append((i+1, text))
    return pages

def chunk_text(text, chunk_size=200, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

if __name__ == "__main__":
    pages = load_pdf(PDF_PATH)
    all_chunks = []
    for page_num, text in pages:
        chunks = chunk_text(text)
        for chunk in chunks:
            all_chunks.append({"page": page_num, "text": chunk})
    print(all_chunks)

