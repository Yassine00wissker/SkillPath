from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from app.config.database import engine, Base
from app.routes import auth, users, formations, parcours, recommend, statistics, jobs
from app.crud import category as crud_category
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.config.database import get_db
from app.core.security import get_current_user, get_current_admin
from app.models.user import User
from app.models.admin import Admin

# Create FastAPI app
app = FastAPI(
    title="SkillPath API",
    description="FastAPI backend for SkillPath learning platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default port
        "http://localhost:3000",  # Alternative React port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(formations.router)
app.include_router(parcours.router)
app.include_router(recommend.router)
app.include_router(statistics.router)
app.include_router(jobs.router)

# Categories router (inline for simplicity)
categories_router = APIRouter(prefix="/categories", tags=["categories"])


@categories_router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category: CategoryCreate, 
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Create a new category (Admin only)."""
    return await crud_category.create_category(db, category)


@categories_router.get("/", response_model=List[CategoryResponse])
async def get_categories(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all categories (Authenticated users only)."""
    categories = await crud_category.get_categories(db, skip=skip, limit=limit)
    return categories


@categories_router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a category by ID (Authenticated users only)."""
    category = await crud_category.get_category(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category


@categories_router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Update a category (Admin only)."""
    category = await crud_category.update_category(db, category_id, category_update)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category


@categories_router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int, 
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Delete a category (Admin only)."""
    success = await crud_category.delete_category(db, category_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return None


app.include_router(categories_router)


@app.on_event("startup")
async def startup():
    """Create database tables on startup."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to SkillPath API"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}

