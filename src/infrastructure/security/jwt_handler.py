import os
from typing import TYPE_CHECKING, Any, Optional, Dict
from datetime import datetime, timedelta, UTC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

import bcrypt
from jose import jwt
from config.config import settings

security_settings = settings.security


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    now: datetime = datetime.now(UTC)
    expire: datetime = now + expires_delta if expires_delta else now + timedelta(minutes=security_settings.jwt_access_token_expire_minutes)

    to_encode: Dict[str, Any] = {"sub": subject, "exp": expire, "iat": now,}
    encoded_jwt: str = jwt.encode(to_encode, security_settings.jwt_secret_key, algorithm=security_settings.jwt_algorithm)
    return encoded_jwt


def create_refresh_token(subject: str) -> str:
    now: datetime = datetime.now(UTC)
    expire: datetime = datetime.now(UTC) + timedelta(days=security_settings.jwt_refresh_token_expire_days)

    to_encode: Dict[str, Any] = {"sub": subject, "exp": expire, "iat": now, "token_type": "refresh"}
    encoded_jwt: str = jwt.encode(to_encode, security_settings.jwt_secret_key, algorithm=security_settings.jwt_algorithm)
    return encoded_jwt


def decode_token(token: str) -> Dict[str, Any]:
    payload = jwt.decode(token, security_settings.jwt_secret_key, algorithms=[security_settings.jwt_algorithm])
    return payload
