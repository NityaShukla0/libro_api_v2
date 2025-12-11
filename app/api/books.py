# app/api/books.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_cache.decorator import cache

from app.crud.crud import create_book, get_book, get_books, update_book, delete_book
from app.schemas.schemas import BookCreate, Book
from app.db.session_manager import get_db_session
from app.config.settings import settings

router = APIRouter(prefix="/books", tags=["Books"])

# Dependency for feature flag
def books_enabled():
    if not settings.ENABLE_BOOKS:
        raise HTTPException(status_code=404, detail="Books API is disabled")


@router.post("/", response_model=Book, summary="Create a new book")
async def api_create_book(
    book: BookCreate,
    db: Session = Depends(get_db_session),
    _=Depends(books_enabled)
):
    """
    Create a new book in the system.
    """
    try:
        return create_book(db, book)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{book_id}", response_model=Book, summary="Get book by ID")
async def api_get_book(
    book_id: int,
    db: Session = Depends(get_db_session),
    _=Depends(books_enabled)
):
    book = get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.get("/", response_model=list[Book], summary="Get all books")
@cache(expire=settings.CACHE_EXPIRE if settings.ENABLE_CACHE else 0)
async def api_get_books(
    db: Session = Depends(get_db_session),
    _=Depends(books_enabled)
):
    return get_books(db)


@router.put("/{book_id}", response_model=Book, summary="Update a book")
async def api_update_book(
    book_id: int,
    book: BookCreate,
    db: Session = Depends(get_db_session),
    _=Depends(books_enabled)
):
    try:
        return update_book(db, book_id, book)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{book_id}", summary="Delete a book")
async def api_delete_book(
    book_id: int,
    db: Session = Depends(get_db_session),
    _=Depends(books_enabled)
):
    try:
        return delete_book(db, book_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))