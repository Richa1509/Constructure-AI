import json
from pathlib import Path
from pypdf import PdfReader

# 1. Where are the PDFs?
BASE_DIR = Path(__file__).parent
DOCS_DIR = BASE_DIR / "docs"
OUTPUT_PATH = BASE_DIR / "index_text.json"

def ingest_docs():
    records = []
    doc_id = 0

    # 2. Loop over all PDFs in docs/
    for pdf_path in DOCS_DIR.glob("*.pdf"):
        print(f"Processing: {pdf_path.name}")
        reader = PdfReader(str(pdf_path))

        # 3. Go page by page
        for page_num, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            text = text.strip()
            if not text:
                # skip pages with no text
                continue

            records.append(
                {
                    "id": doc_id,
                    "file_name": pdf_path.name,
                    "page": page_num,
                    "text": text,
                }
            )
            doc_id += 1

    # 4. Save everything into a JSON file
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    print(f"\nIngestion complete. Saved {len(records)} chunks to {OUTPUT_PATH}")

if __name__ == "__main__":
    ingest_docs()
