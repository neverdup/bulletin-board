from fastapi_pagination import Page, Params, set_page, set_params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select, or_
from sqlalchemy.orm import joinedload
from schemas import PostCreate, PostResponse, PostUpdate
from models import Post, User
from database import get_db
import auth
from typing import Annotated
from fastapi import Depends

CurrentUserDep = Annotated[User, Depends(auth.get_current_user)]


def create_post(post: Post) -> Post:
    session = next(get_db())
    session.add(post)
    session.commit()
    session.refresh(post)

    return post


def get_posts(page: int = 1, size: int = 10, query: str | None = None) -> Page[Post]:
    session = next(get_db())
    set_page(Page[Post])
    set_params(Params(page=page, size=size))

    if query:
        stmt = (
            select(Post)
            .options(joinedload(Post.user))
            .filter(
                or_(Post.title.ilike(f"%{query}%"), Post.content.ilike(f"%{query}%"))
            )
            .order_by(Post.created_at.desc())
        )
    else:
        stmt = (
            select(Post).options(joinedload(Post.user)).order_by(Post.created_at.desc())
        )

    return paginate(
        session,
        stmt,
    )
    # return paginate(session.query(Post).order_by(Post.created_at.desc()))


def get_post(id: int) -> Post:
    session = next(get_db())
    post = session.query(Post).filter(Post.id == id).first()
    return post


def update_post(id: int, update_post: PostUpdate) -> Post:
    session = next(get_db())
    post = session.query(Post).filter(Post.id == id).first()

    if not post:
        return False

    if update_post.title:
        post.title = update_post.title

    if update_post.content:
        post.content = update_post.content

    session.commit()
    session.refresh(post)
    return post


def delete_post(id: int):
    session = next(get_db())
    post = session.query(Post).filter(Post.id == id).first()

    if not post:
        return False

    session.delete(post)
    session.commit()

    return
