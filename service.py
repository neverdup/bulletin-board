from fastapi_pagination import Page, Params, set_page, set_params
from schemas import UserCreate, UserResponse, UserUpdate
from models import User
from database import get_db
from auth import get_password_hash
from typing import Annotated
from fastapi import Depends, Query, HTTPException, status
from main import SessionDep
from sqlalchemy import select
from fastapi_pagination.ext.sqlalchemy import paginate


def create_user(user_create: UserCreate, session: SessionDep) -> User:
    user = User(**user_create.model_dump())
    user.password = get_password_hash(user_create.password)
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


# def get_users(
#     session: SessionDep,
#     offset: int = 0,
#     limit: Annotated[int, Query(le=100)] = 100,
# ) -> list[User]:
#     users = session.query(User).offset(offset).limit(limit).all()
#     return users


def get_users(
    session: SessionDep,
) -> list[User]:
    return paginate(session, select(User).order_by(User.created_at.desc()))


def get_user(user_id: int, session: SessionDep) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


def update_user(user_id: int, update_user: UserUpdate, session: SessionDep) -> User:
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


def delete_user(user_id: int):
    session = next(get_db())
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return
