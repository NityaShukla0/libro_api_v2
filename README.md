# LibroAPI — Transactional Library Management Backend

## Project Summary
LibroAPI is a FastAPI-based backend for a library's catalog and lending system. It supports CRUD for books and users, and transactional borrowing/returning of books with database-level locking to ensure data consistency.

## Tech Stack
- Python 3.10+
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic (migrations)
- pytest + httpx (tests)
- python-dotenv (env management)

## Quickstart (development)
1. Clone the repo and change into it:
   ```bash
   git clone <repo-url>
   cd libro_api_v2