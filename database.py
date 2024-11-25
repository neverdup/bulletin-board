from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session


# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:mysecretpassword@localhost:15432/bulletin-board"


engine = create_engine(
    "postgresql://postgres:mysecretpassword@localhost:15432/bulletin-board"
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


SessionDep = Annotated[Session, Depends(get_db)]
