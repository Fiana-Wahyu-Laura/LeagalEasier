"""
Documents API routes: upload, status, and text retrieval.
"""

import os
import tempfile
import uuid

from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.models.document import Document
from app.services.storage import get_storage_service, StorageService
from app.services.nlp_client import get_nlp_client, NLPServiceClient
from app.schemas.document import DocumentResponse, DocumentStatusResponse, DocumentTextResponse
from sqlalchemy import select

router = APIRouter(prefix="/documents", tags=["documents"])

# File upload constraints
MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB
ALLOWED_MIME_TYPES = {"application/pdf", "image/png", "image/jpeg", "image/tiff"}


@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    storage: StorageService = Depends(get_storage_service),
    nlp_client: NLPServiceClient = Depends(get_nlp_client),
) -> DocumentResponse:
    """
    Upload a document (PDF or image).
    Validates file type and size, saves to storage, creates DB record.
    Returns document ID and status "pending".
    """
    # Validate MIME type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_MIME_TYPES)}",
        )

    # Read file and validate size
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Max size: {MAX_FILE_SIZE / 1024 / 1024} MB",
        )

    # Create document record
    doc_id = uuid.uuid4()
    try:
        # Save file to temp location first
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        # Save to storage service
        storage_path = storage.save_file(tmp_path, file.filename, doc_id)

        # Create DB record
        document = Document(
            id=doc_id,
            filename=file.filename,
            storage_path=storage_path,
            status="pending",
            owner_id=None,  # TODO: Extract from auth token
        )
        db.add(document)
        await db.commit()
        await db.refresh(document)

        # Schedule OCR processing (background task)
        background_tasks.add_task(process_document_ocr, doc_id, storage_path, storage, nlp_client)

        return DocumentResponse.model_validate(document)

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload document: {str(e)}",
        )
    finally:
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.remove(tmp_path)


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> DocumentResponse:
    """Fetch document metadata."""
    stmt = select(Document).where(Document.id == document_id)
    result = await db.execute(stmt)
    document = result.scalar_one_or_none()

    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    return DocumentResponse.model_validate(document)


@router.get("/{document_id}/status", response_model=DocumentStatusResponse)
async def get_document_status(
    document_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> DocumentStatusResponse:
    """Get document processing status."""
    stmt = select(Document).where(Document.id == document_id)
    result = await db.execute(stmt)
    document = result.scalar_one_or_none()

    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    return DocumentStatusResponse(id=document.id, status=document.status)


@router.get("/{document_id}/text", response_model=DocumentTextResponse)
async def get_document_text(
    document_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> DocumentTextResponse:
    """
    Get extracted text from document.
    Returns 202 Accepted if still processing, 200 with text if done, 400 if failed.
    """
    stmt = select(Document).where(Document.id == document_id)
    result = await db.execute(stmt)
    document = result.scalar_one_or_none()

    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    if document.status == "pending" or document.status == "processing":
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED,
            detail="Document is still being processed",
        )

    if document.status == "failed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Document processing failed",
        )

    # Status == "done"
    return DocumentTextResponse(
        id=document.id,
        extracted_text=document.extracted_text or "",
        status=document.status,
    )


async def process_document_ocr(
    document_id: uuid.UUID,
    storage_path: str,
    storage: StorageService,
    nlp_client: NLPServiceClient,
) -> None:
    """
    Background task to process document OCR.
    Calls NLP service (Indra's responsibility) and updates DB with result.
    """
    from app.db.session import AsyncSessionLocal
    try:
        file_path = str(storage.get_file_path(storage_path))

        # Call NLP service for OCR + analysis
        nlp_result = await nlp_client.process_document(document_id, file_path)

        # Update document status and text in DB
        async with AsyncSessionLocal() as db:
            stmt = select(Document).where(Document.id == document_id)
            result = await db.execute(stmt)
            document = result.scalar_one_or_none()

            if document:
                if nlp_result and nlp_result.full_text:
                    document.status = "done"
                    document.extracted_text = nlp_result.full_text
                else:
                    document.status = "failed"
                    document.extracted_text = None

                await db.commit()

    except Exception:
        # Log error and mark as failed
        async with AsyncSessionLocal() as db:
            stmt = select(Document).where(Document.id == document_id)
            result = await db.execute(stmt)
            document = result.scalar_one_or_none()

            if document:
                document.status = "failed"
                await db.commit()
