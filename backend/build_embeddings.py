import json
import os
from pathlib import Path

import numpy as np
from openai import OpenAI

BASE_DIR = Path(__file__).parent
TEXT_INDEX_PATH = BASE_DIR / "index_text.json"
VEC_INDEX_PATH = BASE_DIR / "index_vectors.json"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def embed_text(text: str):
    """Get embedding vector for text."""
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )
    return response.data[0].embedding

def main():
    if not TEXT_INDEX_PATH.exists():
        raise FileNotFoundError("index_text.json not found. Run ingest_text.py first.")

    with open(TEXT_INDEX_PATH, "r", encoding="utf-8") as f:
        records = json.load(f)

    vector_records = []

    for i, rec in enumerate(records, start=1):
        print(f"Embedding {i}/{len(records)} → {rec['file_name']} (page {rec['page']})")
        embedding = embed_text(rec["text"])
        rec_with_vec = {**rec, "embedding": embedding}
        vector_records.append(rec_with_vec)

    with open(VEC_INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(vector_records, f, ensure_ascii=False)

    print("\n✅ Embeddings created successfully!")
    print(f"Saved to → {VEC_INDEX_PATH}")

if __name__ == "__main__":
    main()
