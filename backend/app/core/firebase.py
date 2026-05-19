"""
Firebase Admin SDK initialization and utilities.
"""

import json
import logging
from pathlib import Path

import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin.auth import InvalidIdTokenError, ExpiredIdTokenError, ExpiredSessionCookieError

from app.core.config import get_settings

logger = logging.getLogger(__name__)

_firebase_app = None


def initialize_firebase():
    """Initialize Firebase Admin SDK from credentials file."""
    global _firebase_app
    
    if _firebase_app is not None:
        return
    
    settings = get_settings()
    creds_path = settings.firebase_credentials_path
    
    if not creds_path or not Path(creds_path).exists():
        logger.warning(
            f"Firebase credentials file not found at {creds_path}. "
            "Token verification will be disabled for testing/development."
        )
        return
    
    try:
        creds = credentials.Certificate(creds_path)
        _firebase_app = firebase_admin.initialize_app(creds)
        logger.info("Firebase Admin SDK initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Firebase Admin SDK: {str(e)}")
        raise


def get_firebase_app():
    """Get Firebase app instance (initialize if needed)."""
    global _firebase_app
    if _firebase_app is None:
        initialize_firebase()
    return _firebase_app


async def verify_firebase_token(token: str) -> dict:
    """
    Verify Firebase ID token and return decoded token claims.
    
    Args:
        token: Firebase ID token (without 'Bearer ' prefix)
    
    Returns:
        Decoded token claims including uid, email, etc.
    
    Raises:
        InvalidIdTokenError: Token is invalid or malformed
        ExpiredIdTokenError: Token has expired
        Exception: Other Firebase errors
    """
    try:
        app = get_firebase_app()
        if app is None:
            # Firebase not initialized (dev/test mode); skip verification
            logger.debug("Firebase not initialized; token verification skipped")
            return {}
        
        decoded_token = auth.verify_id_token(token, app=app)
        return decoded_token
    
    except (InvalidIdTokenError, ExpiredIdTokenError, ExpiredSessionCookieError) as e:
        logger.error(f"Firebase token verification failed: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during Firebase token verification: {str(e)}")
        raise
