"""
schemas.py — LegalEasier NLP Pipeline
Pydantic request/response schemas untuk NLP service.

Rules (CLAUDE.md §8):
- Semua endpoint harus mengembalikan format standar { success, data, message }.
- Pydantic models untuk semua request dan response schema — no raw dicts.
"""

from typing import Any

from pydantic import BaseModel, Field


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
# Health check
# ---------------------------------------------------------------------------

class HealthResponse(BaseModel):
    """Response untuk endpoint health check."""

    status: str
    service: str
    version: str
