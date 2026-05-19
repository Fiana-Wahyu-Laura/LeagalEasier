"""
Authentication API routes.
Endpoints for user auth and profile management.
Per CLAUDE.md Section 8: All endpoints except /auth/* require Bearer JWT token.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.schemas.auth import AuthUser

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/me", response_model=AuthUser)
async def get_me(
    current_user: AuthUser = Depends(get_current_user),
) -> AuthUser:
    """
    Get current authenticated user profile.
    
    Requires: Bearer token (Firebase ID token)
    
    Response per CLAUDE.md Section 8:
    - id: UUID of user
    - email: Email address
    - display_name: Optional display name
    - is_active: Account status
    """
    return current_user

