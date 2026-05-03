import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import Base


class Document(Base):
    __tablename__ = "documents"

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id: uuid.UUID | None = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    filename: str = Column(String(1024), nullable=False)
    content: str | None = Column(Text, nullable=True)
    created_at: datetime = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
