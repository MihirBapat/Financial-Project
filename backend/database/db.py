from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# We use a local SQLite file for fast MVP testing today
DATABASE_URL = "sqlite:///./gci_local.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()