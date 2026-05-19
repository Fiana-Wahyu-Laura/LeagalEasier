"""
Pydantic schemas for Document API requests/responses.
"""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):
    """Response schema for document metadata."""

    id: uuid.UUID
    filename: str
    storage_path: str
    status: str
    extracted_text: Optional[str] = None
    summary: Optional[str] = None
    risk_score: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DocumentStatusResponse(BaseModel):
    """Response schema for document status."""

    id: uuid.UUID
    status: str


class DocumentTextResponse(BaseModel):
    """Response schema for extracted text."""

    id: uuid.UUID
    extracted_text: str
    status: str

class RiskClauseResponse(BaseModel):
    clause_text: str
    plain_language: str
    risk_level: str  # "Tinggi", "Sedang", "Rendah", "Aman"
    confidence: float

class DocumentAnalysisResponse(BaseModel):
    document_id: uuid.UUID
    summary: Optional[str] = None
    risk_score: Optional[int] = None
    risk_clauses: list[RiskClauseResponse] = []
    disclaimer: str = "Hasil ini bersifat informatif dan bukan pengganti konsultasi hukum profesional."