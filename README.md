# Constructure AI

## 1. Introduction
Construction documents such as drawings, schedules and specifications contain essential information, but retrieving insights manually is slow and inconsistent. This project implements a simplified document intelligence assistant that enables chat-based document lookup and structured extraction, while running entirely offline.

## 2. Core Capabilities
### Chat over Documents
Users ask natural questions, and the system responds with:
- Relevant document text
- File name and page citation

### Structured Extraction
A demonstration extractor generates a door schedule by scanning and returning structured lines from documents. The design allows additional extractors (room schedules, lists, quantities) to be added easily.

### Retrieval Augmentation (Local RAG)
Rather than relying on external APIs, the system performs:
1. PDF text extraction
2. Local indexing
3. Keyword-based retrieval
4. Response grounding with citations

The architecture is LLM‑ready and can support embedding‑based search when desired.

## 3. Architecture

```
Frontend (Next.js)
 ├─ Chat interface
 └─ Schedule viewer

Backend (FastAPI)
 ├─ PDF ingestion
 ├─ Text indexing
 ├─ Retrieval logic
 ├─ /chat endpoint
 └─ /door-schedule endpoint

Local Data Store
 └─ index_text.json
```

## 4. Workflow Summary
1. PDFs placed in `backend/docs/`
2. Backend ingests and generates `index_text.json`
3. User queries sent from frontend
4. Backend retrieves relevant text chunks
5. UI displays chat responses and citations
6. Extraction endpoint returns structured results for table display

## 5. Setup Instructions

### Backend
```
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install fastapi uvicorn pydantic pypdf numpy
python ingest_text.py
uvicorn main:app --reload --port 8000
```

### Frontend
```
cd frontend
npm install
npm run dev
```

Visit: http://localhost:3000

## 6. API Endpoints

### POST /chat
Returns a grounded answer with source citation.

### POST /door-schedule
Returns extracted lines in structured form. Additional extractors can follow the same interface.

## 7. Design Considerations
- Works offline without external LLMs
- Retrieval layer is modular and replaceable
- UI and backend decoupled through simple JSON APIs
- Extensible for additional document intelligence modules

## 8. Current Status
- Backend functional
- Chat answering enabled
- PDF ingestion working
- Door schedule extracted and displayed
- Citations included for transparency

## 9. Future Work
- UI‑based document uploads
- Embedding‑based retrieval
- Multiple structured extractors
- Ranking improvements
- Conversational memory

## 10. Conclusion
This project demonstrates an end‑to‑end workflow for document intelligence using practical components. It ingests PDFs, retrieves grounded responses and performs structured extraction without external APIs, making it a solid base for future enhancement.
