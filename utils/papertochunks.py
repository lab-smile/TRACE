from PyPDF2 import PdfReader


def extract_text_from_pdf(file_path, verbose=False):
    if verbose:
        print(f"Extracting text from PDF: {file_path}")
    with open(file_path, "rb") as file:
        pdf = PdfReader(file)
        text = " ".join([page.extract_text() for page in pdf.pages])
    if verbose:
        print(f"Extracted {len(text)} characters from PDF")
    return text

def chunkify(path, verbose=False):
    if verbose:
        print(f"Chunkifying text from: {path}")
    chunks = []
    text = extract_text_from_pdf(path, verbose)
    words = text.split()
    for chunk_id, j in enumerate(range(0, len(words), 240), start=1):
        chunk = " ".join(words[j:j+240])
        chunks.append(chunk)
    if verbose:
        print(f"Created {len(chunks)} chunks from the text")
    return chunks


        
    

