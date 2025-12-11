import pytest
from app import crud, schemas
from app.db.database import SessionLocal

@pytest.fixture
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_create_user(db_session):
    user_in = schemas.UserCreate(name="John Doe", email="john@example.com")
    user = crud.create_user(db_session, user_in)
    assert user.name == "John Doe"
    assert user.email == "john@example.com"

def test_create_book(db_session):
    book_in = schemas.BookCreate(
        title="Test Book",
        author="Author A",
        isbn="1234567890",
        publication_year=2025,
        total_copies=3
    )
    book = crud.create_book(db_session, book_in)
    assert book.title == "Test Book"
    assert book.author == "Author A"
    assert book.isbn == "1234567890"

def test_borrow_and_return_book(db_session):
    user = crud.create_user(db_session, schemas.UserCreate(name="Jane", email="jane@example.com"))
    book = crud.create_book(db_session, schemas.BookCreate(
        title="Loan Book",
        author="Author C",
        isbn="555444333",
        publication_year=2025,
        total_copies=1
    ))

    # Borrow the book
    loan = crud.borrow_book(db_session, user.id, book.id)
    assert loan.status == "borrowed"

    # Return the book
    returned_loan = crud.return_book(db_session, user.id, book.id)
    assert returned_loan.status == "returned"