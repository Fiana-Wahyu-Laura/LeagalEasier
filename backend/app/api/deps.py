"""
Shared FastAPI dependencies for auth, db, and other shared services.
"""

import logging
from collections.abc import AsyncGenerator

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.firebase import verify_firebase_token
from app.db.session import get_db_session
from app.models.user import User
from app.schemas.auth import AuthUser

logger = logging.getLogger(__name__)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session for dependency injection."""
    async for session in get_db_session():
        yield session


async def get_current_user(
    authorization: str = Header(None),
    db: AsyncSession = Depends(get_db),
) -> AuthUser:
    """
    Verify Firebase Bearer token and return authenticated user from DB.
    
    Rules per CLAUDE.md Section 8:
    - All endpoints except /auth/* require Bearer JWT token
    - Token validation happens in deps.py get_current_user()
    - Firebase UID is stored in users table, used to link all data
    
    Args:
        authorization: Authorization header (expected format: "Bearer <token>")
        db: Database session
    
    Returns:
        AuthUser: Authenticated user with id, email, display_name, is_active
    
    Raises:
        HTTPException: 401 if no token, invalid token, or user not found in DB
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Parse Bearer token
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format. Expected 'Bearer <token>'",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = authorization[7:]  # Remove "Bearer " prefix
    
    try:
        # Verify Firebase token and extract claims
        decoded_token = await verify_firebase_token(token)
        
        # Extract Firebase UID from token claims
        firebase_uid = decoded_token.get("uid")
        if not firebase_uid:
            logger.warning("Firebase token missing 'uid' claim")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing uid claim",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Look up user in database by Firebase UID
        stmt = select(User).where(User.firebase_uid == firebase_uid)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user:
            logger.warning(f"User not found in DB for Firebase UID: {firebase_uid}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )
        
        return AuthUser.model_validate(user)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error verifying Firebase token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
