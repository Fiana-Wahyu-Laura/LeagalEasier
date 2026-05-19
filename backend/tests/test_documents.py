"""
Integration test for document upload with DB persistence and mocked OCR.
"""

from __future__ import annotations

import asyncio
import time
import uuid
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.api.deps import get_current_user, get_db
from app.api.routes.documents import get_nlp_client, get_storage_service
from app.core.config import get_settings
from app.main import app
from app.models.document import Document
from app.schemas.auth import AuthUser
from app.schemas.nlp import NLPProcessResponse, NLPRiskClause
from app.services.storage import StorageService


class MockNLPClient:
    async def process_document(self, document_id: uuid.UUID, file_path: str) -> NLPProcessResponse:
        return NLPProcessResponse(
            document_id=document_id,
            ocr_used=True,
            full_text="Mock OCR text from integration test",
            summary="Mock summary",
            risk_score=12,
            risk_clauses=[
                NLPRiskClause(
                    clause_text="Mock clause",
                    plain_language="Mock plain language",
                    risk_level="Rendah",
                    confidence=0.99,
                )
            ],
            disclaimer="Hasil ini bersifat informatif dan bukan pengganti konsultasi hukum profesional.",
        )


@pytest.fixture()
def storage_service(tmp_path: Path) -> StorageService:
    return StorageService(storage_root=tmp_path / "storage")


@pytest.fixture(autouse=True)
def override_dependencies(storage_service: StorageService):
    # Mock storage service
    app.dependency_overrides[get_storage_service] = lambda: storage_service
    
    # Mock NLP client
    app.dependency_overrides[get_nlp_client] = lambda: MockNLPClient()
    
    # Mock get_current_user to return a test user (no auth required for tests)
    async def mock_get_current_user():
        return AuthUser(
            id=uuid.uuid4(),
            email="test@example.com",
            display_name="Test User",
            is_active=True,
        )
    
    app.dependency_overrides[get_current_user] = mock_get_current_user
    yield
    app.dependency_overrides.clear()


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)


def wait_for_status(document_id: uuid.UUID, expected_status: str, timeout_seconds: float = 10.0):
    async def _wait() -> dict | None:
        settings = get_settings()
        engine = create_async_engine(str(settings.database_url), future=True)
        SessionLocal = async_sessionmaker(engine, expire_on_commit=False)
        deadline = time.time() + timeout_seconds
        last_payload = None

        try:
            while time.time() < deadline:
                async with SessionLocal() as session:
                    row = await session.get(Document, document_id)
                    last_payload = None if row is None else {"status": row.status, "extracted_text": row.extracted_text}
                    if row is not None and row.status == expected_status:
                        return last_payload
                await asyncio.sleep(0.2)
        finally:
            await engine.dispose()

        pytest.fail(
            f"Document {document_id} did not reach status '{expected_status}' within {timeout_seconds} seconds; last payload={last_payload}"
        )

    return asyncio.run(_wait())


async def cleanup_document(document_id: uuid.UUID) -> None:
    settings = get_settings()
    engine = create_async_engine(str(settings.database_url), future=True)

    async with engine.begin() as conn:
        await conn.execute(delete(Document).where(Document.id == document_id))

    await engine.dispose()


def test_upload_document_persists_and_runs_mock_ocr(client: TestClient, storage_service: StorageService):
    file_content = b"%PDF-1.4\n%Integration test PDF\n"
    files = {"file": ("sample.pdf", file_content, "application/pdf")}

    response = client.post("/api/v1/documents/upload", files=files)

    # Debug: print response if not 201
    if response.status_code != 201:
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
    
    assert response.status_code == 201
    payload = response.json()
    assert payload["filename"] == "sample.pdf"
    assert payload["status"] == "pending"
    assert payload["storage_path"].endswith(".pdf")

    document_id = uuid.UUID(payload["id"])
    stored_file = storage_service.get_file_path(payload["storage_path"])
    assert stored_file.exists()

    document_payload = wait_for_status(document_id, "done")
    assert document_payload["status"] == "done"
    assert document_payload["extracted_text"] == "Mock OCR text from integration test"

    asyncio.run(cleanup_document(document_id))
    stored_file.unlink(missing_ok=True)


def test_health_endpoint(client: TestClient):
    assert client.get("/api/v1/health").status_code == 200
