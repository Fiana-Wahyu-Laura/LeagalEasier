"""
schemas.py — LegalEasier NLP Pipeline
Pydantic request/response schemas untuk NLP service.

Rules (CLAUDE.md §8):
- Semua endpoint harus mengembalikan format standar { success, data, message } untuk endpoint OCR legacy.
- Endpoint kontrak backend ↔ NLP memakai response JSON langsung sesuai `backend/docs/nlp_contract.md`.
- Pydantic models untuk semua request dan response schema — no raw dicts.
"""

from typing import Any, Literal

from pydantic import BaseModel, Field, ConfigDict


# ---------------------------------------------------------------------------
# Standard response wrapper (CLAUDE.md §8)
# ---------------------------------------------------------------------------

class StandardResponse(BaseModel):
    """Wrapper standar untuk semua response NLP service."""

    success: bool
    data: Any | None = None
    message: str


# ---------------------------------------------------------------------------
# OCR Schemas
# ---------------------------------------------------------------------------

class OCRResponse(BaseModel):
    """Response data untuk endpoint OCR extraction."""

    document_id: str = Field(
        description="UUID dokumen yang diproses (dikirim oleh backend)."
    )
    full_text: str = Field(
        description="Teks lengkap hasil ekstraksi / OCR."
    )
    page_count: int = Field(
        description="Jumlah halaman dokumen yang diproses."
    )
    ocr_used: bool = Field(
        description=(
            "True jika Tesseract OCR digunakan (PDF scan / gambar). "
            "False jika teks diekstrak langsung dari PDF digital via PyMuPDF."
        )
    )
    char_count: int = Field(
        description="Jumlah karakter pada full_text (untuk monitoring kualitas OCR)."
    )
    file_type: str = Field(
        description="Tipe file yang diproses: 'pdf', 'jpg', 'jpeg', 'png'."
    )


# ---------------------------------------------------------------------------
# Backend ↔ NLP Contract Schemas (Sprint 2)
# ---------------------------------------------------------------------------

FileType = Literal["pdf", "jpg", "png", "docx"]
RiskLevel = Literal["Tinggi", "Sedang", "Rendah", "Aman"]


class NLPProcessRequest(BaseModel):
    """Metadata yang dikirim backend saat memproses dokumen."""

    document_id: str
    file_type: FileType


class NLPRiskClause(BaseModel):
    clause_text: str
    plain_language: str
    risk_level: RiskLevel
    confidence: float = Field(ge=0.0, le=1.0)


class NLPProcessResponse(BaseModel):
    document_id: str
    ocr_used: bool
    full_text: str
    summary: str
    risk_score: int = Field(ge=0, le=100)
    risk_clauses: list[NLPRiskClause]
    disclaimer: str

    model_config = ConfigDict(extra="ignore")


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

class HealthResponse(BaseModel):
    """Response untuk endpoint health check."""

    status: str
    service: str
    version: str
