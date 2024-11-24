from typing import Annotated
from database import SessionDep
from models import User
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi import HTTPException, status
from schemas import UserCreate, UserUpdate
from auth import get_password_hash


def create_user(user_create: UserCreate, session: Session) -> User:
    user = User(**user_create.model_dump())
    user.password = get_password_hash(user_create.password)
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def get_users(
    session: Session,
) -> list[User]:
    return paginate(session, select(User).order_by(User.created_at.desc()))


def get_user(user_id: int, session: Session) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


def update_user(user_id: int, update_user: UserUpdate, session: Session) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if update_user.name:
        user.name = update_user.name

    if update_user.email:
        user.email = update_user.email

    session.commit()
    session.refresh(user)

    return user


def delete_user(user_id: int, session: Session):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return
