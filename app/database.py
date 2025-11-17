# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# This is the correct default database URL for your Docker setup
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://app_user:app_password@db:5432/app_db",
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
