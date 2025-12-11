# app/api/loans.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_cache.decorator import cache

from app.crud.crud import create_loan, return_loan, get_loans
from app.schemas.schemas import BookBorrowRequest, BookReturnRequest, LoanResponse
from app.db.session_manager import get_db_session
from app.config.settings import settings

router = APIRouter(prefix="/loans", tags=["Loans"])

# Dependency for feature flag
def loans_enabled():
    if not settings.ENABLE_BORROW or not settings.ENABLE_RETURN:
        raise HTTPException(status_code=404, detail="Loan API is disabled")


@router.post("/borrow", response_model=LoanResponse, summary="Borrow a book")
async def api_borrow_book(
    book_id: int,
    request: BookBorrowRequest,
    db: Session = Depends(get_db_session),
    _=Depends(loans_enabled)
):
    """
    Borrow a book by providing the book_id and user_id.
    """
    try:
        return create_loan(db, book_id, request.user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/return", response_model=LoanResponse, summary="Return a borrowed book")
async def api_return_book(
    request: BookReturnRequest,
    db: Session = Depends(get_db_session),
    _=Depends(loans_enabled)
):
    """
    Return a borrowed book using the loan_id.
    """
    try:
        return return_loan(db, request.loan_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[LoanResponse], summary="Get all loans")
@cache(expire=settings.CACHE_EXPIRE if settings.ENABLE_CACHE else 0)
async def api_get_loans(
    db: Session = Depends(get_db_session),
    _=Depends(loans_enabled)
):
    """
    Retrieve all loan records.
    """
    try:
        return get_loans(db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))