from .pdf_loader import load_pdf, chunk_text


def ingest_pdf(pdf_path, store, embedder):
    pages = load_pdf(pdf_path)
    all_texts = []
    all_metadata = []
    for page_num, text in pages:
        chunks = chunk_text(text)
        for idx, chunk in enumerate(chunks):
            all_texts.append(chunk)
            all_metadata.append({
                "source": pdf_path,
                "page": page_num,
                "chunk_index": idx,
            })
    vectors = embedder.encode(all_texts)
    store.addDocument(all_texts, vectors, all_metadata)
    return len(all_texts)
