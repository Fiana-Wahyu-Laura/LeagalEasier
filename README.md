# LegalEasier

> Penerjemah Dokumen Hukum ke Bahasa Awam Berbasis AI

LegalEasier adalah aplikasi mobile berbasis AI yang membantu masyarakat umum memahami dokumen hukum Indonesia (kontrak kerja, perjanjian sewa, akta jual beli, dan lainnya) tanpa perlu latar belakang hukum.

> ⚠️ LegalEasier bukan pengganti konsultan hukum profesional. Seluruh hasil analisis bersifat informatif dan edukatif.

---

## Status

**Sprint 1** — In progress

| Sprint | Fokus | Status |
| ------ | ----- | ------ |
| Sprint 1 | Auth (Flutter + Backend), OCR (NLP), Database schema | 🔄 In progress |
| Sprint 2 | Upload dokumen, preprocessing, embedding | ⏳ Belum dimulai |
| Sprint 3 | Analisis risiko LLM, detail dokumen | ⏳ Belum dimulai |
| Sprint 4 | RAG chatbot, limit guest | ⏳ Belum dimulai |
| Sprint 5 | History, UI polish | ⏳ Belum dimulai |

---

## Tech Stack

| Layer       | Teknologi                                                |
| ----------- | ---------------------------------------------------------|
| Mobile      | Flutter 3.x + Riverpod + go_router                       |
| Backend API | FastAPI (Python 3.11) + PostgreSQL 16                    |
| File Storage| PostgreSQL bytea — served via `GET /documents/{id}/file` |
| NLP & AI    | PyMuPDF, Tesseract OCR, SpaCy, LangChain, ChromaDB       |
| LLM         | Claude API (primary) + GPT-4 (fallback)                  |
| Auth        | Firebase Auth (Google + Email/Password)                  |

---

## Struktur Repo

```
LeagalEasier/
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
├── backend/                         # FastAPI REST API
│   ├── app/
│   │   ├── api/routes/              # Endpoint routes
│   │   ├── core/                    # Config & security
│   │   ├── models/                  # SQLAlchemy models
│   │   └── schemas/                 # Pydantic schemas
│   └── alembic/                     # DB migrations
├── nlp_pipeline/                    # NLP & AI microservice (port 8001)
│   ├── core/                        # Config (pydantic-settings)
│   ├── ocr/                         # PyMuPDF + Tesseract OCR ✅ Sprint 1
│   ├── preprocessing/               # Text preprocessing (Sprint 2)
│   ├── rag/                         # Retrieval-Augmented Generation (Sprint 2)
│   ├── llm/                         # LLM integration — Claude API (Sprint 3)
│   ├── tests/                       # Unit tests
│   ├── main.py                      # FastAPI entry point
│   └── schemas.py                   # Pydantic schemas
├── database/                        # SQL schema & migrations
│   └── migrations/
├── docker-compose.yml
└── requirements.txt
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

> Panduan setup lengkap per service akan ditambahkan di masing-masing folder (`frontend/README.md`, `backend/README.md`, `nlp_pipeline/README.md`) seiring development berjalan.

Untuk saat ini, mulai dari:

```bash
git clone https://github.com/Fiana-Wahyu-Laura/LeagalEasier.git
cd LeagalEasier
```

Lalu ikuti instruksi di folder sesuai jobdesk masing-masing.

---

## Tim

| Nama                 | NIM        | Jobdesk                                              |
| -------------------- | ---------- | ---------------------------------------------------- |
| Ester Faninta        | 2301020053 | Frontend: Flutter UI, Firebase Auth                  |
| Fiana Wahyu Laura    | 2301020082 | Frontend: Flutter UI, Firebase Auth                  |
| Masry Ryzki Yanditar | 2301020087 | Backend: FastAPI, PostgreSQL, File Storage           |
| Jamalludin           | 2301020075 | Backend: FastAPI, PostgreSQL, File Storage           |
| Indra Sugara         | 2301020084 | AI/NLP: OCR, RAG, LLM, ChromaDB                      |

> **Catatan:** File storage (dokumen upload) ditangani Backend via PostgreSQL bytea.
> Frontend hanya kirim file sebagai multipart ke backend.

---

## Git Workflow

```bash
git checkout main && git pull origin main

# ... kerjakan ...

git add .
git commit -m "feat: deskripsi singkat"
git push
# buat Pull Request ke main
```

Format commit: `feat` / `fix` / `refactor` / `style` / `docs` / `test` / `chore`

---

## Mata Kuliah

**Pemrograman Perangkat Mobile**

> Teknik Informatika - Universitas Maritim Raja Ali Haji, 2026
