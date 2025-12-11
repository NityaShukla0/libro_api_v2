# LibroAPI v2 — README

## Project overview

**Project name:** LibroAPI v2

**Short description:**
A transactional Library Management System built with FastAPI, SQLAlchemy and PostgreSQL. The API supports user and book management plus transactional borrow/return operations with database integrity guaranteed through SQL transactions.

**Scope & purpose:**

* Track users and books
* Create/read/update books and users
* Borrow and return books with transactional safety (ensure `available_copies` never goes below 0, consistent loan records, rollback on failure)
* Provide a minimal, testable backend suitable for extension (auth, notifications, admin UI)

---

## Repository contents (recommended layout)

libro_api_v2/

* app/

  * api/

    * books.py
    * users.py
    * loans.py
  * crud/

    * crud.py
  * db/

    * database.py
  * models/

    * models.py
  * schemas/

    * schemas.py
  * utils/

    * exceptions.py
  * main.py
* tests/

  * conftest.py
  * test_books.py
  * test_crud.py
  * test_loans.py
  * test_users.py
* alembic/ (optional)
* create_tables.py (optional helper)
* requirements.txt
* .env.example
* README.md

---

## README goals for the repo (what this file provides)

1. Project purpose and scope (above)
2. Setup instructions (PostgreSQL, virtualenv, requirements, .env example)
3. How to run the application and API examples (curl)
4. How to run tests
5. Self-reflection (what you learned and transactional rationale)

---

## Prerequisites

* Python 3.10+ (3.11/3.14 will also work but ensure compatibility with dependencies)
* PostgreSQL 12+
* `git`, `pip` and `virtualenv` or `python -m venv`

---

## Environment (.env example)

Create a `.env` in the project root with these values (example):

```
DATABASE_URL=postgresql+psycopg2://libro_user:libro_pass@localhost:5432/libro_db
# Optional: for tests you can override to use sqlite file or in-memory
TEST_DATABASE_URL=sqlite:///./test.db

# App settings
APP_HOST=127.0.0.1
APP_PORT=8000

# Alembic config (if using migrations)
ALEMBIC_DATABASE_URL=${DATABASE_URL}
```

Make sure you create the PostgreSQL database and user before running the app:

```bash
# Example (postgres user):
psql -U postgres
CREATE USER libro_user WITH PASSWORD 'libro_pass';
CREATE DATABASE libro_db OWNER libro_user;
GRANT ALL PRIVILEGES ON DATABASE libro_db TO libro_user;
\q
```

---

## Setup (local development)

1. Clone the repo

```
git clone https://github.com/<your-org>/libro_api_v2.git
cd libro_api_v2
```

2. Create and activate virtualenv

Mac/Linux:

```
python3 -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell):

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies

```
pip install -r requirements.txt
```

4. Create `.env` as shown above and ensure `DATABASE_URL` points to a running PostgreSQL instance.

5. (Optional) Initialize DB schema

* If you use SQLAlchemy `Base.metadata.create_all(bind=engine)` or `create_tables.py` that imports models and calls `Base.metadata.create_all(bind=engine)`, run it once:

```
python create_tables.py
```

* If using Alembic for migrations:

```
alembic upgrade head
```

---

## Running the application

Development (uvicorn reload):

```
uvicorn app.main:app --reload
```

Open docs at `http://127.0.0.1:8000/docs` or `http://127.0.0.1:8000/redoc`.

---

## API endpoints (examples)

Base URL: `http://127.0.0.1:8000`

### Users

Create user (POST /users/)

```
curl -X POST "http://127.0.0.1:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "email": "alice@example.com"}'
```

Get all users (GET /users/)

```
curl http://127.0.0.1:8000/users/
```

Get user by id (GET /users/{user_id})

```
curl http://127.0.0.1:8000/users/1
```

### Books

Create book (POST /books/)

```
curl -X POST "http://127.0.0.1:8000/books/" \
  -H "Content-Type: application/json" \
  -d '{"title": "Deep Learning", "author": "Ian Goodfellow", "isbn": "9780262035613", "publication_year": 2016, "total_copies": 3}'
```

Get book by id (GET /books/{book_id})

```
curl http://127.0.0.1:8000/books/1
```

### Loans (borrow/return)

Borrow a book (POST /loans/borrow/{user_id}/{book_id}) — example using numeric ids returned when you create user/book

```
# If user id is 2 and book id is 5:
curl -X POST "http://127.0.0.1:8000/loans/borrow/2/5"
```

Return a book (POST /loans/return/{loan_id}) — if you return using loan id

```
curl -X POST "http://127.0.0.1:8000/loans/return/10"
```

Or if your API accepts return by user and book

```
curl -X POST "http://127.0.0.1:8000/loans/return/2/5"
```

**Notes for borrow/return examples:**

* Borrow must check `available_copies > 0` and run inside the same DB transaction that creates a loan record and decrements `available_copies` — failing either step should rollback both.
* Return must update `return_date`, change `status` and increment `available_copies` also within a transaction.

---

## Running tests

1. Ensure `TEST_DATABASE_URL` is configured in `.env` or `pytest.ini` points to a sqlite URL for isolated tests.
2. Install dev/test dependencies: `pip install -r requirements.txt` (if tests need additional packages add them in `requirements.txt`).
3. Run pytest:

```
python -m pytest -q
```

Common failures and debug tips:

* `AttributeError: module 'app.crud' has no attribute 'create_user'`: check `app/crud/__init__.py` exports, ensure functions are defined in `crud.py` and imported in `__init__.py`.
* `ModuleNotFoundError: No module named 'app'` when running uvicorn from the wrong working directory — `cd` into the repo root (where the `app` package folder sits) before starting uvicorn.
* `relation "users" does not exist`: run your migrations or `create_tables.py` to create tables before testing endpoints that write to DB.

---

## Example: curl walk-through (create user, book, borrow, return)

1. Create a user

```
curl -s -X POST "http://127.0.0.1:8000/users/" -H "Content-Type: application/json" -d '{"name":"Bob", "email":"bob@example.com"}'
```

Response:

```
{"id": 3, "name": "Bob", "email": "bob@example.com"}
```

2. Create a book

```
curl -s -X POST "http://127.0.0.1:8000/books/" -H "Content-Type: application/json" -d '{"title":"Python 101","author":"Author","isbn":"111222333","publication_year":2022,"total_copies":2}'
```

Response:

```
{"id": 5, "title":"Python 101", "available_copies": 2, ...}
```

3. Borrow the book

```
curl -s -X POST "http://127.0.0.1:8000/loans/borrow/3/5"
```

Expected success response: a loan object with `status: "borrowed"` and `borrow_date` set. `available_copies` for book decremented to 1.

4. Return the book

```
curl -s -X POST "http://127.0.0.1:8000/loans/return/{loan_id}"
```

Response: loan object now includes `return_date` and `status: "returned"` and `available_copies` increments back.

---

## Git & release notes

1. Initialize git and push to GitHub

```
git init
git add .
git commit -m "Initial commit — LibroAPI v2"
# create repo on GitHub then:
git remote add origin git@github.com:<username>/libro_api_v2.git
git push -u origin main
```

2. Tag releases if desired

```
git tag -a v1.0.0 -m "Initial public release"
git push origin v1.0.0
```

---

## Self-reflection (short)

What I learned:

* How to structure a small yet maintainable FastAPI project with layered concerns (routes, CRUD, models, schemas).
* Proper use of SQLAlchemy sessions and the importance of explicit transactions when coupling multiple DB operations.
* How to write tests that exercise the database layer and API layer using pytest and TestClient.

Why transactions matter here:

* Borrowing a book requires two changes: creating a loan record and decrementing the `available_copies` on the book. If either fails (e.g., constraint violation, or another process sold out copies), a partial update would corrupt the state. Wrapping both operations in a single DB transaction ensures atomicity: either both succeed or neither do.

Challenges & how I overcame them:

* Debugging import errors and circular imports: resolved by reorganizing package-level exports (use `app.crud.__init__` to re-export functions) and ensuring app entrypoint is run from the project root.
* Schema/tables not present during tests: added `create_tables.py` and recommended running migrations in README so tests have tables.
* Unique constraint errors when re-running manual curl tests — addressed by checking for existing resources first in the API or using idempotent endpoints for tests.

---

## TODO / Next steps

* Add authentication (JWT) and r
