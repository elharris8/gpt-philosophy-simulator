import fitz  # PyMuPDF

def extract_pdf_text(filepath):
    doc = fitz.open(filepath)
    text = ""
    for page in doc:
        # Get blocks and extract text from each block
        blocks = page.get_text("blocks")  # Returns a list of text blocks
        for block in blocks:
            text += block[4] + "\n"  # Block text is at index 4
    doc.close()
    return text