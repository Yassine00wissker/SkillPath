from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.database import get_db
from app.models.user import User
from app.models.admin import Admin

# Lazy imports will be used inside functions to avoid circular dependencies

# Secret key for JWT - In production, use environment variable
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    # Check if the hash is already a bcrypt hash (starts with $2b$)
    if hashed_password.startswith("$2b$") or hashed_password.startswith("$2a$"):
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    # For compatibility with passlib format
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    # Generate salt and hash password
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    """Decode and verify a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Get the current authenticated user from JWT token."""
    # Lazy import to avoid circular dependency
    from app.crud.user import get_user
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = decode_access_token(token)
        email: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        user_type: str = payload.get("type", "user")  # "user" or "admin"
        
        if email is None or user_id is None:
            raise credentials_exception
        
        if user_type == "admin":
            # Admins should use get_current_admin instead
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required. Use /auth/admin/login endpoint."
            )
        
        user = await get_user(db, user_id)
        if user is None:
            raise credentials_exception
        
        return user
    except JWTError:
        raise credentials_exception


async def get_current_admin(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> Admin:
    """Get the current authenticated admin from JWT token."""
    # Lazy import to avoid circular dependency
    from app.crud import admin as crud_admin
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = decode_access_token(token)
        email: str = payload.get("sub")
        admin_id: int = payload.get("user_id")
        user_type: str = payload.get("type", "user")
        
        if email is None or admin_id is None:
            raise credentials_exception
        
        if user_type != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
        
        admin = await crud_admin.get_admin_by_email(db, email)
        if admin is None:
            raise credentials_exception
        
        return admin
    except JWTError:
        raise credentials_exception


