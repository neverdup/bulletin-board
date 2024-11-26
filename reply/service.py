from fastapi_pagination import Page
import reply.repository as repo
from schemas import ReplyCreate, PostOut, PostUpdate
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


# def update_post(
#     id: int,
#     update_post: PostUpdate,
#     current_user: CurrentUserDep,
# ):
#     post = repo.get_post(id)

#     if not post:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Post not found",
#         )

#     if current_user.id != post.user_id:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Not allowed to update other's post",
#         )

#     post = repo.update_post(
#         id,
#         update_post,
#     )

#     return post


# def delete_post(
#     id: int,
#     current_user: CurrentUserDep,
# ):

#     post = repo.get_post(id)

#     if not post:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Post not found",
#         )

#     if current_user.id != post.user_id:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Not allowed to delete other's post",
#         )

#     repo.delete_post(id)
