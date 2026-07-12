from pypdf import PdfReader
from pprint import pprint
from sample_Text import SAMPLE_TEXT

PDF_PATH = "/Users/abdulsamadgilal/Development/Vector-Search-Engine/vector-search-youtube/pdfs/Abdul_Samad_Gilal.pdf"

def pdf_loader(file_path):
    reader = PdfReader(file_path)
    pages = []
    for index, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            pages.append((index+1, text))
    return pages

def chunks(text, chunk_size = 200, overlap = 50):
    word = text.split()
    chunks = []
    for i in range(0,len(word), chunk_size - overlap):
        chunk = " ".join(word[i:i+chunk_size])
        chunks.append(chunk)
    return chunks




if __name__ == "__main__":
    data = pdf_loader(file_path= PDF_PATH)
    # pprint(dir(data.pages[0]))
    # pprint(dir(data))
    # page_01 = data.pages[1].extract_text()
    # print(page_01)
    # print(data.pages)
    # pprint(data)
    chunks = chunks(text=SAMPLE_TEXT)
    pprint(chunks)
