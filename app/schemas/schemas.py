from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ------------------------
# Book Schemas
# ------------------------
class BookBase(BaseModel):
    title: str
    author: str
    isbn: str
    publication_year: int
    total_copies: int

class BookCreate(BookBase):
    pass

# Added BookUpdate for updating existing books
class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    publication_year: Optional[int] = None
    total_copies: Optional[int] = None

class Book(BookBase):
    id: int
    available_copies: int

    class Config:
        from_attributes = True

# ------------------------
# User Schemas
# ------------------------
class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

# ------------------------
# Loan Schemas
# ------------------------
class LoanBase(BaseModel):
    book_id: int
    user_id: int
    borrow_date: Optional[datetime]
    due_date: Optional[datetime]
    return_date: Optional[datetime]
    status: str

class LoanCreate(BaseModel):
    book_id: int
    user_id: int

class Loan(LoanBase):
    id: int

    class Config:
        from_attributes = True

class LoanResponse(BaseModel):
    id: int
    book_id: int
    user_id: int
    borrow_date: Optional[datetime]
    due_date: Optional[datetime]
    return_date: Optional[datetime]
    status: str

    class Config:
        from_attributes = True

# ------------------------
# Request Schemas for Borrow/Return
# ------------------------
class BookBorrowRequest(BaseModel):
    user_id: int

class BookReturnRequest(BaseModel):
    loan_id: int