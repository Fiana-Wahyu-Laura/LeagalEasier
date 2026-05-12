"""
Authentication API routes.
Stub implementation for non-blocking frontend development.
TODO: Integrate Firebase token verification.
"""

import uuid
from fastapi import APIRouter, Header, HTTPException, status

router = APIRouter(prefix="/auth", tags=["auth"])


class CurrentUser:
    """Placeholder user for stub auth."""

    def __init__(self):
        self.id: uuid.UUID = uuid.uuid4()
        self.email: str = "placeholder@legaleasier.dev"
        self.name: str = "Placeholder User"
        self.is_active: bool = True


@router.get("/me")
async def get_current_user(
    authorization: str = Header(None),
) -> dict:
    """
    Get current authenticated user.
    Stub: Returns placeholder user if no auth header.
    TODO: Verify Firebase token and return actual user.
    """
    if not authorization:
        # Stub: Return placeholder user for non-blocking frontend dev
        user = CurrentUser()
        return {
            "id": str(user.id),
            "email": user.email,
            "name": user.name,
            "is_active": user.is_active,
        }

    # TODO: Parse Bearer token and verify with Firebase
    # For now, just accept any token and return placeholder
    try:
        if authorization.startswith("Bearer "):
            # In future: verify_firebase_token(authorization[7:])
            user = CurrentUser()
            return {
                "id": str(user.id),
                "email": user.email,
                "name": user.name,
                "is_active": user.is_active,
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization header format",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
