# app/models/models.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.db.database import Base
from enum import Enum
from datetime import datetime

# -----------------------
# Enum for Loan status
# -----------------------
class LoanStatusEnum(str, Enum):
    BORROWED = "borrowed"
    RETURNED = "returned"

# -----------------------
# User model
# -----------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    loans = relationship("Loan", back_populates="user")

# -----------------------
# Book model
# -----------------------
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    isbn = Column(String, unique=True, nullable=False)
    publication_year = Column(Integer, nullable=False)
    total_copies = Column(Integer, nullable=False)
    available_copies = Column(Integer, nullable=False)

    loans = relationship("Loan", back_populates="book")

# -----------------------
# Loan model
# -----------------------
class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    borrow_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    return_date = Column(DateTime, nullable=True)

    # ✅ use SQLAlchemy Enum for status
    status = Column(SQLEnum(LoanStatusEnum), default=LoanStatusEnum.BORROWED, nullable=False)

    user = relationship("User", back_populates="loans")
    book = relationship("Book", back_populates="loans")