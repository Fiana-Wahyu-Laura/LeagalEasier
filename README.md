# LegalEasier

> Penerjemah Dokumen Hukum ke Bahasa Awam Berbasis AI

LegalEasier adalah aplikasi mobile berbasis AI yang membantu masyarakat umum memahami dokumen hukum Indonesia (kontrak kerja, perjanjian sewa, akta jual beli, dan lainnya) tanpa perlu latar belakang hukum.

> LegalEasier bukan pengganti konsultan hukum profesional. Seluruh hasil analisis bersifat informatif dan edukatif.

---

## Status (19 Mei 2026)

| Sprint   | Fokus                                                | Status           | Progress |
| -------- | ---------------------------------------------------- | ---------------- | -------- |
| Sprint 1 | Auth (Flutter + Backend), OCR (NLP), Database schema | Sebagian Selesai | ~60%     |
| Sprint 2 | Upload dokumen, preprocessing, embedding, RAG        | In Progress      | ~70%     |
| Sprint 3 | Analisis risiko LLM, detail dokumen                  | In Progress      | ~50%     |
| Sprint 4 | RAG chatbot, limit guest                             | Belum dimulai    | —        |
| Sprint 5 | History, UI polish                                   | Belum dimulai    | —        |
| Sprint 6 | Integration & optimization                           | Belum dimulai    | —        |

---

## Tech Stack

| Layer        | Teknologi                                                  |
| ------------ | ---------------------------------------------------------- |
| Mobile       | Flutter 3.x + Riverpod 2.x + go_router                     |
| Backend API  | FastAPI + SQLAlchemy 2.x (async) + PostgreSQL 16           |
| File Storage | PostgreSQL `bytea` — served via `GET /documents/{id}/file` |
| OCR          | PyMuPDF (digital) + Tesseract (scanned)                    |
| NLP          | SpaCy + NLTK + LangChain Text Splitter                     |
| Embedding    | sentence-transformers (all-MiniLM-L6-v2)                   |
| Vector DB    | ChromaDB (persistence)                                     |
| RAG          | LangChain + LangGraph                                      |
| LLM          | Claude API (primary) + GPT-4 (fallback)                    |
| Auth         | Firebase Auth (Google + Email/Password) + JWT              |

---

## Struktur Repo

```
LegalEasier/
├── frontend/                        # Flutter mobile app
│   ├── lib/
│   │   ├── core/
│   │   │   ├── constants/
│   │   │   ├── router/
│   │   │   ├── theme/
│   │   │   └── utils/
│   │   └── features/
│   │       ├── analysis/            # Analisis dokumen
│   │       ├── auth/                # Login & register
│   │       ├── chatbot/             # Chat AI
│   │       ├── document/            # Upload & manajemen dokumen
│   │       └── onboarding/          # Onboarding screen
│   ├── assets/                      # Icons, images, animations
│   └── test/
├── backend/                         # FastAPI REST API (port 8000)
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/              # auth, documents, analysis, chat endpoints
│   │   │   └── deps.py              # JWT & DB dependencies
│   │   ├── core/
│   │   │   ├── config.py            # Settings (pydantic-settings)
│   │   │   ├── security.py          # JWT utils
│   │   │   └── firebase.py          # Firebase Admin SDK
│   │   ├── db/                      # Database session
│   │   ├── models/                  # SQLAlchemy ORM (User, Document, etc)
│   │   ├── schemas/                 # Pydantic request/response schemas
│   │   └── services/                # Business logic layer
│   ├── alembic/                     # Database migrations
│   │   └── versions/
│   ├── tests/                       # Integration & unit tests
│   ├── storage/                     # Local document storage (2026/)
│   ├── requirements.txt
│   └── .env.example
├── nlp_pipeline/                    # NLP & AI microservice (port 8001)
│   ├── core/
│   │   └── config.py                # Settings (pydantic-settings)
│   ├── ocr/                         # PyMuPDF + Tesseract OCR
│   │   ├── pdf_extractor.py         # Digital PDF extraction (Selesai)
│   │   └── image_ocr.py             # Scanned PDF/image OCR (Selesai)
│   ├── preprocessing/               # Indonesian text preprocessing (Selesai)
│   │   ├── cleaner.py               # Text normalization (Selesai)
│   │   ├── tokenizer.py             # SpaCy tokenization (Selesai)
│   │   └── splitter.py              # Sentence splitting (Selesai)
│   ├── rag/                         # Retrieval-Augmented Generation (Selesai)
│   │   ├── chunker.py               # LangChain splitter (512 tokens, overlap 50) (Selesai)
│   │   ├── embedder.py              # sentence-transformers embeddings (Selesai)
│   │   ├── vector_store.py          # ChromaDB operations (Selesai)
│   │   └── retriever.py             # Semantic search (Selesai)
│   ├── llm/                         # LLM integration & analysis (Selesai)
│   │   ├── analyzer.py              # Risk clause detection (Selesai)
│   │   ├── translator.py            # Plain language translation (Selesai)
│   │   ├── risk_scorer.py           # Risk score generation (0-100) (Selesai)
│   │   └── prompts.py               # System prompts untuk Claude API (Selesai)
│   ├── tests/                       # 145/145 unit tests passed (Selesai)
│   │   ├── test_ocr_extractor.py
│   │   ├── test_preprocessing.py
│   │   ├── test_rag_pipeline.py
│   │   └── test_llm_pipeline.py
│   ├── chroma_db/                   # ChromaDB persistent storage
│   ├── main.py                      # FastAPI entry point
│   ├── schemas.py                   # Pydantic schemas
│   ├── requirements.txt
│   └── .env.example
├── database/
│   ├── schema.sql                   # Full DB schema (source of truth)
│   └── migrations/
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Prasyarat

| Tool           | Versi  | Link                                                 |
| -------------- | ------ | ---------------------------------------------------- |
| Flutter SDK    | 3.x    | https://docs.flutter.dev/get-started/install/windows |
| Python         | 3.11+  | https://www.python.org/downloads/                    |
| PostgreSQL     | 16     | https://www.postgresql.org/download/windows/         |
| Tesseract OCR  | latest | https://github.com/UB-Mannheim/tesseract/wiki        |
| Android Studio | latest | https://developer.android.com/studio                 |
| Git            | latest | https://git-scm.com/download/win                     |

> **Tesseract (Windows):** Install ke `C:\Program Files\Tesseract-OCR\` lalu tambahkan ke PATH.

---

## Setup

### Quick Start

```bash
git clone https://github.com/Fiana-Wahyu-Laura/LegalEasier.git
cd LegalEasier
```

### Per Service

**Frontend (Flutter)**

```bash
cd frontend
flutter pub get
flutter run
```

**Backend (FastAPI)**

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**NLP Pipeline (FastAPI microservice)**

```bash
cd nlp_pipeline
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
# Download SpaCy model (first time only):
python -m spacy download xx_ent_wiki_sm
# Download NLTK resources (first time only):
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords'); nltk.download('wordnet')"
# Run tests (optional):
pytest tests/ -v
# Start server:
uvicorn main:app --reload --port 8001
```

> Backend dan NLP Pipeline punya venv **terpisah** — jangan dicampur!

---

## Tim Developer

| Nama                 | NIM        | Jobdesk                                    |
| -------------------- | ---------- | ------------------------------------------ |
| Ester Faninta        | 2301020053 | Frontend: Flutter UI, Firebase Auth        |
| Fiana Wahyu Laura    | 2301020082 | Frontend: Flutter UI, Firebase Auth        |
| Masry Ryzki Yanditar | 2301020087 | Backend: FastAPI, PostgreSQL, File Storage |
| Jamalludin           | 2301020075 | Backend: FastAPI, PostgreSQL, File Storage |
| Indra Sugara         | 2301020084 | NLP/AI: OCR, RAG, LLM, ChromaDB            |

---

## Mata Kuliah

**Pemrograman Perangkat Mobile** (2026)

Teknik Informatika — Universitas Maritim Raja Ali Haji
