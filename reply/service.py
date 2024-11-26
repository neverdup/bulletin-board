from fastapi_pagination import Page
import reply.repository as repo
from schemas import ReplyCreate, ReplyUpdate
from models import Post, User, Reply
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import Depends, HTTPException, status
import auth

CurrentUserDep = Annotated[User, Depends(auth.get_current_user)]


def create_reply(user_id: int, reply_create: ReplyCreate):
    reply = Reply(**reply_create.model_dump())
    reply.user_id = user_id
    reply = repo.create_reply(reply)
    return reply


# def get_posts(page: int = 1, size: int = 10, query: str | None = None) -> Page[Post]:
#     posts = repo.get_posts(
#         page=page,
#         size=size,
#         query=query,
#     )
#     return posts


# def get_post(id: int) -> Post:
#     post = repo.get_post(id)
#     return post


def update_reply(
    id: int,
    update_reply: ReplyUpdate,
    current_user: User,
):
    reply = repo.update_reply(
        id,
        update_reply,
        current_user,
    )

    return reply


def delete_post(
    id: int,
    current_user: CurrentUserDep,
):
    repo.delete_reply(id, current_user)
    return
