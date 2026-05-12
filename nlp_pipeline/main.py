"""
main.py — LegalEasier NLP Pipeline
FastAPI entry point untuk NLP microservice (port 8001).

Menjalankan:
    uvicorn main:app --reload --port 8001

Endpoints Sprint 1:
    GET  /health           → health check
    POST /ocr/extract      → OCR extraction (PyMuPDF + Tesseract fallback)

Endpoints Sprint 2 contract:
    POST /nlp/process      → backend ↔ NLP contract response

Rules (CLAUDE.md):
- Semua endpoint kecuali /health memerlukan validasi dari backend (Sprint 2+).
- Semua response menggunakan format standar { success, data, message }.
- Error handling: jangan expose stack trace ke response.
- Pydantic models untuk semua request/response — no raw dicts.
"""

import logging
import uuid
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, File, Form, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from ocr.image_ocr import extract_text_from_image, extract_text_from_pdf_scan
from ocr.pdf_extractor import extract_text_from_pdf
from schemas import (
    HealthResponse,
    NLPProcessRequest,
    NLPProcessResponse,
    NLPRiskClause,
    OCRResponse,
    StandardResponse,
)

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Lifespan
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Jalankan startup/shutdown tasks."""
    logger.info("NLP Pipeline service dimulai di port %d.", settings.service_port)
    yield
    logger.info("NLP Pipeline service dihentikan.")


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(
    title="LegalEasier NLP Pipeline",
    description=(
        "Microservice untuk OCR, preprocessing, RAG, dan analisis dokumen hukum Indonesia. "
        "Sprint 1: OCR extraction (PyMuPDF + Tesseract)."
    ),
    version="0.1.0",
    lifespan=lifespan,
)

# CORS — izinkan backend (port 8000) memanggil service ini
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Allowed file types
# ---------------------------------------------------------------------------

ALLOWED_FILE_TYPES = {"pdf", "jpg", "jpeg", "png"}


def _validate_file_type(file_type: str) -> str:
    """Validasi dan normalisasi tipe file."""
    normalized = file_type.lower().lstrip(".")
    if normalized not in ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Tipe file tidak didukung: '{file_type}'. "
                   f"Gunakan salah satu dari: {', '.join(ALLOWED_FILE_TYPES)}.",
        )
    return normalized


def _validate_file_size(file_bytes: bytes) -> None:
    """Validasi ukuran file tidak melebihi batas maksimum."""
    if len(file_bytes) > settings.max_file_size_bytes:
        max_mb = settings.max_file_size_bytes // (1024 * 1024)
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Ukuran file melebihi batas maksimum {max_mb}MB.",
        )


def _build_nlp_contract_response(
    doc_id: str,
    normalized_type: str,
    full_text: str,
    ocr_used: bool,
) -> NLPProcessResponse:
    """Bangun response kontrak backend ↔ NLP menggunakan output OCR yang tersedia saat ini."""

    return NLPProcessResponse(
        document_id=doc_id,
        ocr_used=ocr_used,
        full_text=full_text,
        summary=(
            "Ringkasan sementara: dokumen berhasil diproses dan teks berhasil diekstrak. "
            "Analisis lanjutan akan diisi pada Sprint 3."
        ),
        risk_score=0,
        risk_clauses=[],
        disclaimer="Hasil ini bersifat informatif dan bukan pengganti konsultasi hukum profesional.",
    )


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    tags=["System"],
)
async def health_check() -> HealthResponse:
    """Cek status NLP service. Tidak memerlukan autentikasi."""
    return HealthResponse(
        status="ok",
        service="legaleasier-nlp-pipeline",
        version="0.1.0",
    )


@app.post(
    "/ocr/extract",
    response_model=StandardResponse,
    summary="OCR Extraction",
    tags=["OCR"],
    status_code=status.HTTP_200_OK,
)
async def ocr_extract(
    file: UploadFile = File(..., description="File dokumen (PDF, JPG, PNG)."),
    file_type: str = Form(..., description="Tipe file: 'pdf', 'jpg', 'jpeg', 'png'."),
    document_id: str = Form(
        default="",
        description="UUID dokumen dari backend (opsional, untuk tracking).",
    ),
) -> StandardResponse:
    """
    Ekstrak teks dari dokumen menggunakan OCR pipeline:
    1. Untuk PDF → coba PyMuPDF terlebih dahulu (teks digital).
    2. Jika PyMuPDF gagal / teks kosong → fallback ke Tesseract OCR.
    3. Untuk gambar (JPG/PNG) → langsung Tesseract OCR.

    Mengembalikan teks lengkap dan flag `ocr_used` yang menandakan
    apakah Tesseract digunakan (True) atau tidak (False).
    """
    # Gunakan UUID random jika document_id tidak dikirim
    doc_id = document_id if document_id else str(uuid.uuid4())

    # Baca konten file
    file_bytes: bytes = await file.read()

    # Validasi tipe & ukuran
    normalized_type = _validate_file_type(file_type)
    _validate_file_size(file_bytes)

    logger.info(
        "Memproses dokumen '%s' (tipe=%s, ukuran=%d bytes).",
        doc_id,
        normalized_type,
        len(file_bytes),
    )

    try:
        if normalized_type == "pdf":
            # Langkah 1: Coba ekstrak teks digital via PyMuPDF
            pdf_result = extract_text_from_pdf(file_bytes)

            if pdf_result.full_text:
                # PDF digital — teks berhasil diekstrak tanpa OCR
                ocr_data = OCRResponse(
                    document_id=doc_id,
                    full_text=pdf_result.full_text,
                    page_count=pdf_result.page_count,
                    ocr_used=False,
                    char_count=len(pdf_result.full_text),
                    file_type=normalized_type,
                )
            else:
                # Langkah 2: PDF scan — fallback ke Tesseract
                logger.info(
                    "PyMuPDF tidak menemukan teks pada '%s'. Fallback ke Tesseract OCR.",
                    doc_id,
                )
                ocr_result = extract_text_from_pdf_scan(file_bytes)
                ocr_data = OCRResponse(
                    document_id=doc_id,
                    full_text=ocr_result.full_text,
                    page_count=ocr_result.page_count,
                    ocr_used=True,
                    char_count=len(ocr_result.full_text),
                    file_type=normalized_type,
                )

        else:
            # JPG / PNG — langsung Tesseract
            ocr_result = extract_text_from_image(file_bytes, file_type=normalized_type)
            ocr_data = OCRResponse(
                document_id=doc_id,
                full_text=ocr_result.full_text,
                page_count=ocr_result.page_count,
                ocr_used=True,
                char_count=len(ocr_result.full_text),
                file_type=normalized_type,
            )

    except ValueError as exc:
        # File tidak valid (bukan PDF/gambar yang dapat dibuka)
        logger.warning("File tidak valid untuk dokumen '%s': %s", doc_id, exc)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:
        # Tesseract tidak ditemukan atau error teknis lainnya
        logger.error("Runtime error saat memproses dokumen '%s': %s", doc_id, exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Gagal memproses dokumen. Silakan coba lagi atau hubungi administrator.",
        ) from exc

    method = "Tesseract OCR" if ocr_data.ocr_used else "PyMuPDF (teks digital)"
    logger.info(
        "Dokumen '%s' berhasil diproses via %s: %d karakter.",
        doc_id,
        method,
        ocr_data.char_count,
    )

    return StandardResponse(
        success=True,
        data=ocr_data.model_dump(),
        message=f"Ekstraksi teks berhasil menggunakan {method}.",
    )


@app.post(
    "/nlp/process",
    response_model=NLPProcessResponse,
    summary="Backend ↔ NLP contract endpoint",
    tags=["NLP"],
    status_code=status.HTTP_200_OK,
)
async def nlp_process(
    file: UploadFile = File(..., description="File dokumen (PDF, JPG, PNG)."),
    file_type: str = Form(..., description="Tipe file: 'pdf', 'jpg', 'jpeg', 'png'."),
    document_id: str = Form(..., description="UUID dokumen dari backend."),
) -> NLPProcessResponse:
    """
    Endpoint kontrak backend ↔ NLP.

    Untuk saat ini, endpoint ini memakai pipeline OCR yang sama dengan `/ocr/extract`
    dan mengembalikan response JSON langsung tanpa wrapper standar.
    """

    request_meta = NLPProcessRequest(document_id=document_id, file_type=_validate_file_type(file_type))
    file_bytes: bytes = await file.read()
    _validate_file_size(file_bytes)

    normalized_type = request_meta.file_type

    try:
        if normalized_type == "pdf":
            pdf_result = extract_text_from_pdf(file_bytes)

            if pdf_result.full_text:
                full_text = pdf_result.full_text
                ocr_used = False
            else:
                logger.info(
                    "PyMuPDF tidak menemukan teks pada '%s'. Fallback ke Tesseract OCR.",
                    request_meta.document_id,
                )
                ocr_result = extract_text_from_pdf_scan(file_bytes)
                full_text = ocr_result.full_text
                ocr_used = True
        else:
            ocr_result = extract_text_from_image(file_bytes, file_type=normalized_type)
            full_text = ocr_result.full_text
            ocr_used = True

    except ValueError as exc:
        logger.warning("File tidak valid untuk dokumen '%s': %s", request_meta.document_id, exc)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:
        logger.error("Runtime error saat memproses dokumen '%s': %s", request_meta.document_id, exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Gagal memproses dokumen. Silakan coba lagi atau hubungi administrator.",
        ) from exc

    return _build_nlp_contract_response(
        doc_id=request_meta.document_id,
        normalized_type=normalized_type,
        full_text=full_text,
        ocr_used=ocr_used,
    )
