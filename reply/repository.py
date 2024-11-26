from fastapi_pagination import Page, Params, set_page, set_params
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi import HTTPException, status
from sqlalchemy import select, or_
from sqlalchemy.orm import joinedload
from schemas import PostCreate, PostOut, PostUpdate
from models import Reply, User
from database import get_db


def create_reply(reply: Reply) -> Reply:
    session = next(get_db())
    session.add(reply)
    session.commit()
    session.refresh(reply)

    return reply


# def get_posts(page: int = 1, size: int = 10, query: str | None = None) -> Page[Post]:
#     session = next(get_db())
#     set_page(Page[Post])
#     set_params(Params(page=page, size=size))

#     if query:
#         stmt = (
#             select(Post)
#             .options(joinedload(Post.user))
#             .filter(
#                 or_(Post.title.ilike(f"%{query}%"), Post.content.ilike(f"%{query}%"))
#             )
#             .order_by(Post.created_at.desc())
#         )
#     else:
#         stmt = (
#             select(Post).options(joinedload(Post.user)).order_by(Post.created_at.desc())
#         )

#     return paginate(
#         session,
#         stmt,
#     )
#     # return paginate(session.query(Post).order_by(Post.created_at.desc()))


def get_reply(id: int) -> Reply:
    session = next(get_db())
    reply = session.query(Reply).filter(Reply.id == id).first()
    return reply


def update_reply(
    id: int,
    update_reply: Reply,
    current_user: User,
) -> Reply:
    session = next(get_db())
    reply = session.query(Reply).filter(Reply.id == id).first()

    if not reply:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    if current_user.id != reply.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not allowed to update other's reply",
        )

    if update_reply.content:
        reply.content = update_reply.content

    session.commit()
    session.refresh(reply)
    return reply


def delete_reply(
    id: int,
    current_user: User,
):
    session = next(get_db())
    reply = session.query(Reply).filter(Reply.id == id).first()

    if not reply:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    if current_user.id != reply.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not allowed to delete other's post",
        )

    session.delete(reply)
    session.commit()

    return
