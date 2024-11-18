from fastapi_pagination import Page
import post.repository as repo
from schemas import PostCreate, PostResponse, PostUpdate
from models import Post, User
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import Depends, HTTPException, status
import auth

CurrentUserDep = Annotated[User, Depends(auth.get_current_user)]


def create_post(user_id: int, post_create: PostCreate):
    post = Post(**post_create.model_dump())
    post.user_id = user_id
    post = repo.create_post(post)
    return post


def get_posts(page: int = 1, size: int = 10, query: str | None = None) -> Page[Post]:
    posts = repo.get_posts(
        page=page,
        size=size,
        query=query,
    )
    return posts


def get_post(id: int) -> Post:
    post = repo.get_post(id)
    return post


def update_post(
    id: int,
    update_post: PostUpdate,
    current_user: CurrentUserDep,
):
    post = repo.get_post(id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    if current_user.id != post.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not allowed to update other's post",
        )

    post = repo.update_post(
        id,
        update_post,
    )

    return post


def delete_post(
    id: int,
    current_user: CurrentUserDep,
):

    post = repo.get_post(id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    if current_user.id != post.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not allowed to delete other's post",
        )

    repo.delete_post(id)
