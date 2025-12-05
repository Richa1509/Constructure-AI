from pypdf import PdfReader
from pathlib import Path

# Point to the docs folder
docs_dir = Path(__file__).parent / "docs"
pdf_path = docs_dir / "sample.pdf"   # change name if your file is different

print(f"Looking for PDF at: {pdf_path}")

# Open the PDF
reader = PdfReader(str(pdf_path))

print(f"Total number of pages: {len(reader.pages)}")

# Print preview of each page
for page_num, page in enumerate(reader.pages, start=1):
    text = page.extract_text() or ""
    preview = text[:300].replace("\n", " ")
    print(f"\n--- Page {page_num} ---")
    print(preview if preview else "[No text extracted]")

