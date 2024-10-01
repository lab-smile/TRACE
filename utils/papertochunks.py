from PyPDF2 import PdfReader


def extract_text_from_pdf(file_path, verbose=False):
    """Extract text from a PDF file."""
    if verbose:
        print(f"Extracting text from PDF: {file_path}")
    with open(file_path, "rb") as file:
        pdf = PdfReader(file)
        text = " ".join(page.extract_text() for page in pdf.pages)
    if verbose:
        print(f"Extracted {len(text)} characters from PDF")
    return text

def chunkify(path, verbose=False, chunk_size=240):
    """Split the text from a PDF into chunks."""
    if verbose:
        print(f"Chunkifying text from: {path}")
    text = extract_text_from_pdf(path, verbose)
    words = text.split()
    chunks = [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    if verbose:
        print(f"Created {len(chunks)} chunks from the text")
    return chunks


        
    

