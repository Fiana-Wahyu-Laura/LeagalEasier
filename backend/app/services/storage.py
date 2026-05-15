"""
Storage service for handling file uploads.
Supports local disk storage by default; extensible for S3/GCS.
"""

import os
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from app.core.config import get_settings


class StorageService:
    """Local disk storage handler."""

    def __init__(self, storage_root: str | Path | None = None):
        self.settings = get_settings()
        self.storage_root = Path(storage_root or self.settings.storage_root)
        self.storage_root.mkdir(parents=True, exist_ok=True)

    def _get_storage_path(self, original_filename: str, document_id: uuid.UUID) -> tuple[str, Path]:
        """
        Generate storage path and relative path for a document.
        Format: YYYY/MM/DD/<document_id>.<extension>
        Returns: (relative_path_for_db, absolute_path_on_disk)
        """
        now = datetime.now(timezone.utc)
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")

        # Extract file extension
        _, ext = os.path.splitext(original_filename)
        if not ext:
            ext = ".bin"  # Default if no extension

        # Build relative path for database storage_path column
        relative_path = f"{year}/{month}/{day}/{document_id}{ext}"

        # Build absolute filesystem path
        abs_path = self.storage_root / relative_path

        return relative_path, abs_path

    def save_file(
        self, file_path: str, original_filename: str, document_id: uuid.UUID
    ) -> str:
        """
        Save uploaded file to storage.
        Args:
            file_path: Temporary path where file was saved
            original_filename: Original filename from upload
            document_id: UUID of document record

        Returns:
            relative_path: Path to store in database (e.g., "2026/05/11/<uuid>.pdf")
        """
        relative_path, abs_path = self._get_storage_path(original_filename, document_id)

        # Create directory if not exists
        abs_path.parent.mkdir(parents=True, exist_ok=True)

        # Copy file from temp location to storage
        shutil.copy2(file_path, abs_path)

        return relative_path

    def get_file_path(self, storage_path: str) -> Path:
        """
        Get absolute path for a stored file.
        Args:
            storage_path: Relative path from database (e.g., "2026/05/11/<uuid>.pdf")

        Returns:
            Absolute path on filesystem
        """
        return self.storage_root / storage_path

    def delete_file(self, storage_path: str) -> bool:
        """Delete a file from storage."""
        file_path = self.get_file_path(storage_path)
        try:
            if file_path.exists():
                file_path.unlink()
                return True
        except Exception:
            pass
        return False

    def file_exists(self, storage_path: str) -> bool:
        """Check if file exists in storage."""
        return self.get_file_path(storage_path).exists()


def get_storage_service() -> StorageService:
    """Dependency injection for storage service."""
    return StorageService()
