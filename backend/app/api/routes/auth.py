"""
Authentication API routes.
Endpoints for user auth and profile management.
Per CLAUDE.md Section 8: All endpoints except /auth/* require Bearer JWT token.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.schemas.auth import AuthUser, AuthRegisterRequest, AuthLoginRequest, AuthTokenResponse
from app.models.user import User
from app.core.firebase import get_firebase_app
import uuid

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthTokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: AuthRegisterRequest,
    db: AsyncSession = Depends(get_db),
) -> AuthTokenResponse:
    """
    Register a new user account.
    
    Requires: Email and password
    
    Response per CLAUDE.md Section 8:
    - user: User profile (id, email, display_name, is_active)
    - token: Firebase custom token for authentication
    
    Raises:
        400: Invalid email format or password too short
        409: Email already registered
    """
    try:
        # Check if email already exists
        stmt = select(User).where(User.email == request.email)
        result = await db.execute(stmt)
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )
        
        # Create user in Firebase
        app = get_firebase_app()
        if app is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Firebase not initialized",
            )
        
        from firebase_admin import auth as firebase_auth
        
        try:
            firebase_user = firebase_auth.create_user(
                email=request.email,
                password=request.password,
                app=app,
            )
            firebase_uid = firebase_user.uid
        except firebase_auth.EmailAlreadyExistsError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )
        except firebase_auth.WeakPasswordError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password is too weak",
            )
        except Exception as e:
            logger.error(f"Firebase user creation failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user",
            )
        
        # Create user in database
        new_user = User(
            id=uuid.uuid4(),
            firebase_uid=firebase_uid,
            email=request.email,
            display_name=request.display_name,
            is_active=True,
        )
        
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        
        # Generate Firebase custom token
        custom_token = firebase_auth.create_custom_token(firebase_uid, app=app)
        
        return AuthTokenResponse(
            user=AuthUser.model_validate(new_user),
            token=custom_token.decode() if isinstance(custom_token, bytes) else custom_token,
        )
    
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed",
        )


@router.post("/login", response_model=AuthTokenResponse)
async def login(
    request: AuthLoginRequest,
    db: AsyncSession = Depends(get_db),
) -> AuthTokenResponse:
    """
    Login with email and password.
    
    Requires: Email and password
    
    Response per CLAUDE.md Section 8:
    - user: User profile (id, email, display_name, is_active)
    - token: Firebase custom token for authentication
    
    Raises:
        401: Invalid email or password
        403: User account is inactive
    """
    try:
        # Look up user in database
        stmt = select(User).where(User.email == request.email)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )
        
        # Verify password with Firebase
        app = get_firebase_app()
        if app is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Firebase not initialized",
            )
        
        from firebase_admin import auth as firebase_auth
        
        try:
            firebase_auth.get_user_by_email(request.email, app=app)
            # User exists; verify password by generating custom token
            custom_token = firebase_auth.create_custom_token(user.firebase_uid, app=app)
        except firebase_auth.UserNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        except Exception as e:
            logger.error(f"Firebase authentication failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        
        return AuthTokenResponse(
            user=AuthUser.model_validate(user),
            token=custom_token.decode() if isinstance(custom_token, bytes) else custom_token,
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )


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

