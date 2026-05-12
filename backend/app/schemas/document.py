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
