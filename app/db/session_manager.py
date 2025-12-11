# app/db/session_manager.py

from sqlalchemy.orm import Session
from app.db.database import SessionLocal

def get_db_session():
    """
    Dependency for FastAPI endpoints to provide a database session.
    Usage in a route:
        def route(db: Session = Depends(get_db_session)):
            ...
    Commits/rollbacks should be handled in the CRUD functions.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()