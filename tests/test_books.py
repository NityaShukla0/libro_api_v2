import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import SessionLocal
@pytest.fixture
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@pytest.fixture
def client(db_session):
    # Override get_db dependency
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides = {}
    from app.db.database import get_db
    app.dependency_overrides[get_db] = _override_get_db
    yield TestClient(app)
    app.dependency_overrides = {}
def test_create_user_api(client):
    response = client.post("/users/", json={"name": "API User", "email": "apiuser@example.com"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "API User"
    assert data["email"] == "apiuser@example.com"
def test_create_book_api(client):
    response = client.post("/books/", json={
        "title": "API Book",
        "author": "API Author",
        "isbn": "111222333",
        "publication_year": 2025,
        "total_copies": 2
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "API Book"
    assert data["author"] == "API Author"
    assert data["isbn"] == "111222333"
def test_borrow_book_api(client):
    # Create user and book
    user_resp = client.post("/users/", json={"name": "Borrower", "email": "borrower@example.com"})
    book_resp = client.post("/books/", json={
        "title": "Borrow Book",
        "author": "Author B",
        "isbn": "999888777",
        "publication_year": 2025,
        "total_copies": 1
    })
    user_id = user_resp.json()["id"]
    book_id = book_resp.json()["id"]
    # Borrow the book
    borrow_resp = client.post(f"/loans/borrow/{user_id}/{book_id}")
    assert borrow_resp.status_code == 200
    data = borrow_resp.json()
    assert data["user_id"] == user_id
    assert data["book_id"] == book_id
    assert data["status"] == "borrowed"