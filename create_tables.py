import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.database import Base, engine
from app import models

# Create all tables
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
