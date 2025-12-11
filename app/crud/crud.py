# app/crud/crud.py

from sqlalchemy.orm import Session
from datetime import datetime
from app.models.models import User, Book, Loan, LoanStatusEnum

# -------------------
# Loans CRUD
# -------------------
def create_loan(db: Session, book_id: int, user_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book or book.available_copies <= 0:
        raise Exception("Book not available")
    loan = Loan(user_id=user_id, book_id=book_id, status=LoanStatusEnum.BORROWED)
    book.available_copies -= 1
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan

def return_loan(db: Session, loan_id: int):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan or loan.status != LoanStatusEnum.BORROWED:
        raise Exception("Loan not valid for return")
    loan.status = LoanStatusEnum.RETURNED
    loan.return_date = datetime.utcnow()
    book = db.query(Book).filter(Book.id == loan.book_id).first()
    if book:
        book.available_copies += 1
    db.commit()
    db.refresh(loan)
    return loan

def get_loans(db: Session):
    return db.query(Loan).all()


# -------------------
# Users CRUD
# -------------------
def create_user(db: Session, user_data):
    user = User(name=user_data.name, email=user_data.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session):
    return db.query(User).all()


# -------------------
# Books CRUD
# -------------------
def create_book(db: Session, book_data):
    book = Book(
        title=book_data.title,
        author=book_data.author,
        isbn=book_data.isbn,
        publication_year=book_data.publication_year,
        total_copies=book_data.total_copies,
        available_copies=book_data.total_copies
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

def get_book(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()

def get_books(db: Session):
    return db.query(Book).all()

def update_book(db: Session, book_id: int, book_data):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise Exception("Book not found")
    
    # Update fields
    book.title = book_data.title
    book.author = book_data.author
    book.isbn = book_data.isbn
    book.publication_year = book_data.publication_year
    
    # Adjust copies
    diff = book_data.total_copies - book.total_copies
    book.total_copies = book_data.total_copies
    book.available_copies += diff
    
    db.commit()
    db.refresh(book)
    return book

def delete_book(db: Session, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise Exception("Book not found")
    db.delete(book)
    db.commit()
    return {"detail": "Book deleted successfully"}