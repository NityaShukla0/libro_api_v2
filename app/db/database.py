# app/db/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg2://nityashukla:password123@db:5432/libro_db"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Import all models here so that they are registered with Base
from app.models import models  # ✅ ensure all models are imported

# Dependency to get DB session in FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create all tables in the database
def init_db():
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")

# Run this only if script executed directly
if __name__ == "__main__":
    init_db()