"""
Schemas for the backend ↔ NLP service contract.
"""

from __future__ import annotations

from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


FileType = Literal["pdf", "jpg", "png", "docx"]
RiskLevel = Literal["Tinggi", "Sedang", "Rendah", "Aman"]


class NLPProcessRequest(BaseModel):
    """Metadata fields sent alongside the multipart file upload."""

    document_id: UUID
    file_type: FileType


class NLPRiskClause(BaseModel):
    clause_text: str
    plain_language: str
    risk_level: RiskLevel
    confidence: float = Field(ge=0.0, le=1.0)


class NLPProcessResponse(BaseModel):
    document_id: UUID
    ocr_used: bool
    full_text: str
    summary: str
    risk_score: int = Field(ge=0, le=100)
    risk_clauses: list[NLPRiskClause]
    disclaimer: str

    model_config = ConfigDict(extra="ignore")
