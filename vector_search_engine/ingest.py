from .pdf_loader import load_pdf, chunk_text


def ingest_pdf(pdf_path, store, embedder):
    pages = load_pdf(pdf_path)
    all_texts = []
    all_metadata = []
    for page_num, text in pages:
        text_chunks = chunk_text(text)
        for idx, chunk in enumerate(text_chunks):
            all_texts.append(chunk)
            all_metadata.append({
                "source": pdf_path,
                "page": page_num,
                "chunk_index": idx,
            })
    vectors = embedder.encode(all_texts)
    store.addDocument(all_texts, vectors, all_metadata)
    return len(all_texts)


# Backward-compatible alias
ingest = ingest_pdf
