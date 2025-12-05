from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import json

app = FastAPI()

# Allow frontend (Next.js) to call this backend from localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----- Load text index (from ingest_text.py) -----
BASE_DIR = Path(__file__).parent
TEXT_INDEX_PATH = BASE_DIR / "index_text.json"

if TEXT_INDEX_PATH.exists():
    with open(TEXT_INDEX_PATH, "r", encoding="utf-8") as f:
        TEXT_INDEX = json.load(f)
    print(f"Loaded {len(TEXT_INDEX)} chunks from {TEXT_INDEX_PATH}")
else:
    TEXT_INDEX = []
    print("WARNING: index_text.json not found. Run ingest_text.py first.")


# ----- Simple keyword retrieval -----
def simple_retrieve(query: str, k: int = 5):
    """
    Very simple keyword-based retrieval:
    score = how many query words appear in the chunk text.
    """
    if not TEXT_INDEX:
        return []

    q_tokens = [t.lower() for t in query.split() if t.strip()]
    scored = []

    for item in TEXT_INDEX:
        text_lower = item["text"].lower()
        score = sum(1 for t in q_tokens if t in text_lower)
        if score > 0:
            scored.append((score, item))

    # sort by score (highest first)
    scored.sort(key=lambda x: x[0], reverse=True)

    return [item for score, item in scored[:k]]


# ----- API models & routes -----
class ChatRequest(BaseModel):
    message: str
class DoorScheduleRequest(BaseModel):
    query: str | None = None  # optional, default "door schedule"
@app.post("/door-schedule")
def door_schedule(req: DoorScheduleRequest):
    """
    Very simple 'door schedule' extractor:
    - Uses keyword retrieval (door / schedule)
    - Splits relevant chunks into lines
    - Returns each line as a structured row
    """
    base_query = req.query or "door schedule"

    # retrieve chunks that likely contain door info
    hits = simple_retrieve(base_query, k=10)

    if not hits:
        return {
            "rows": [],
            "citations": [],
            "note": "No relevant text found for door schedule.",
        }

    rows = []

    for h in hits:
        text = h["text"]
        # split into lines to get schedule-like rows
        for raw_line in text.splitlines():
            line = raw_line.strip()
            # simple heuristic: keep lines that mention 'door' or look like a mark
            if not line:
                continue
            lower = line.lower()
            if "door" in lower or "d-" in lower or "door " in lower:
                rows.append(
                    {
                        "file_name": h["file_name"],
                        "page": h["page"],
                        "line": line,
                    }
                )

    citations = [
        {"file_name": h["file_name"], "page": h["page"]}
        for h in hits
    ]

    return {
        "rows": rows,
        "citations": citations,
        "note": (
            "This is a simple keyword-based extraction of lines that look door-related. "
            "In a production system an LLM would convert this into richer structured fields."
        ),
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(req: ChatRequest):
    user_query = req.message

    hits = simple_retrieve(user_query, k=5)

    if not hits:
        return {
            "answer": (
                "I searched the project documents but couldn't find anything "
                "matching your question."
            ),
            "citations": [],
        }

    top = hits[0]
    snippet = top["text"][:600]

    answer = (
        "I am running in keyword-search-only mode (no external AI API available). "
        "Here is the most relevant text I found in the project documents "
        "for your question:\n\n"
        f"{snippet}\n\n"
        f"(From {top['file_name']}, page {top['page']})"
    )

    citations = [
        {"file_name": h["file_name"], "page": h["page"]}
        for h in hits
    ]

    return {
        "answer": answer,
        "citations": citations,
    }
