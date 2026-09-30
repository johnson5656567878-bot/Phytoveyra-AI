import hashlib
import hmac
from datetime import datetime, timedelta, timezone
from typing import Any, Union, Optional
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login", auto_error=False)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Use SHA-256 with key hashing for password verification
    expected = hashlib.sha256((plain_password + settings.JWT_SECRET).encode('utf-8')).hexdigest()
    return hmac.compare_digest(expected, hashed_password)

def get_password_hash(password: str) -> str:
    return hashlib.sha256((password + settings.JWT_SECRET).encode('utf-8')).hexdigest()

def create_access_token(subject: Union[str, Any], role: str = "Farmer", expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "role": role,
        "type": "access_token"
    }
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
