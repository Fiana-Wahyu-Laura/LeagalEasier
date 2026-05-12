"""
NLP service client for OCR processing.
Handles communication with Indra's NLP pipeline service.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional, cast
from uuid import UUID

import httpx

from app.core.config import get_settings
from app.schemas.nlp import FileType, NLPProcessRequest, NLPProcessResponse

logger = logging.getLogger(__name__)


class NLPServiceClient:
    """Client for NLP/OCR service integration."""

    def __init__(self):
        self.settings = get_settings()
        self.base_url = str(self.settings.nlp_service_url)
        self.timeout = 300  # 5 minutes for OCR processing

    @staticmethod
    def _detect_file_type(file_path: str) -> FileType:
        suffix = Path(file_path).suffix.lower().lstrip(".")
        if suffix in {"pdf", "jpg", "png", "docx"}:
            return cast(FileType, suffix)

        # Default to pdf-like handling when the extension is unknown.
        return "pdf"

    @staticmethod
    def _mime_type_for_file_type(file_type: FileType) -> str:
        return {
            "pdf": "application/pdf",
            "jpg": "image/jpeg",
            "png": "image/png",
            "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        }[file_type]

    async def process_document(
        self,
        document_id: UUID,
        file_path: str,
    ) -> Optional[NLPProcessResponse]:
        """
        Send document to NLP service for OCR + analysis processing.

        The agreed multipart contract is:
        - document_id: UUID
        - file_type: pdf|jpg|png|docx
        - file: binary file bytes

        Returns the parsed JSON payload from NLP or None if the service fails.
        """
        try:
            file_type = self._detect_file_type(file_path)
            request = NLPProcessRequest(document_id=document_id, file_type=file_type)

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                with open(file_path, "rb") as f:
                    files = {
                        "file": (
                            Path(file_path).name,
                            f,
                            self._mime_type_for_file_type(request.file_type),
                        )
                    }
                    data = {
                        "document_id": str(request.document_id),
                        "file_type": request.file_type,
                    }

                    response = await client.post(
                        f"{self.base_url}/nlp/process",
                        files=files,
                        data=data,
                    )

                    if response.status_code == 200:
                        return NLPProcessResponse.model_validate(response.json())
                    else:
                        logger.error(
                            f"NLP service error for {document_id}: {response.status_code} {response.text}"
                        )
                        return None

        except httpx.TimeoutException:
            logger.error(f"NLP service timeout for document {document_id}")
            return None
        except Exception as e:
            logger.error(f"NLP service error for document {document_id}: {str(e)}")
            return None


def get_nlp_client() -> NLPServiceClient:
    """Dependency injection for NLP client."""
    return NLPServiceClient()
