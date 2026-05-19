"""
Authentication schemas.
"""

import uuid
from pydantic import BaseModel, EmailStr


class AuthUser(BaseModel):
    """Authenticated user response schema."""
    id: uuid.UUID
    email: str
    display_name: str | None = None
    is_active: bool

    class Config:
        from_attributes = True
