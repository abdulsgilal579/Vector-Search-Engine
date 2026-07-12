from pdf_loader import pdf_loader, chunks
from pprint import pprint

def ingest(pdf_path, store, embedding):
    data = pdf_loader(pdf_path)
    all_text = []
    all_metadatas = []
    for page_number, text in data:
        text_chunks = chunks(text)
        for index, chunk in enumerate(text_chunks):
            all_text.append(chunk)
            all_metadatas.append({
                "source": pdf_path,
                "page_number": page_number,
                "index": index
            })
    vector = embedding.encode(all_text)
    store.addDocument(all_text, vector, all_metadatas)
    return len(all_text)


if __name__ == "__main__":
    PDF_PATH = "/Users/abdulsamadgilal/Development/Vector-Search-Engine/vector-search-youtube/pdfs/Abdul_Samad_Gilal.pdf"
    data = ingest(pdf_path=PDF_PATH)
    pprint(data)

