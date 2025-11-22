from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from app.config.database import get_db
from app.crud.user import get_user_by_email, create_user
from app.crud.admin import get_admin_by_email
from app.schemas.user import UserCreate, UserResponse
from app.schemas.admin import AdminResponse
from app.core.security import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["authentication"])


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class AdminToken(BaseModel):
    access_token: str
    token_type: str
    admin: AdminResponse


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user."""
    # Check if email already exists
    existing_user = await get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    new_user = await create_user(db, user)
    return new_user


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    Login and get access token.
    Note: OAuth2PasswordRequestForm uses 'username' field for email.
    Send as form data: username=email@example.com&password=yourpassword
    Or use JSON with Content-Type: application/x-www-form-urlencoded
    """
    # OAuth2PasswordRequestForm uses 'username' field, but we use email
    email = form_data.username
    
    # Get user by email
    user = await get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Verify password
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id, "type": "user"},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.model_validate(user)
    }


@router.post("/admin/login", response_model=AdminToken)
async def admin_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    Login as admin and get access token.
    Note: OAuth2PasswordRequestForm uses 'username' field for email.
    Send as form data: username=email@example.com&password=yourpassword
    """
    # OAuth2PasswordRequestForm uses 'username' field, but we use email
    email = form_data.username
    
    # Get admin by email
    admin = await get_admin_by_email(db, email)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Verify password
    if not verify_password(form_data.password, admin.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": admin.email, "user_id": admin.id, "type": "admin"},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "admin": AdminResponse.model_validate(admin)
    }
