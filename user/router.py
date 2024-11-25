from typing import Annotated
from fastapi import APIRouter, Depends, Request, status, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_pagination import Page, Params
from sqlalchemy.orm import Session

from auth import get_current_user, CurrentUserDep
from database import SessionDep
from models import User
from schemas import UserCreate, UserOut, UserUpdate
from user import service

router = APIRouter(prefix="/user", tags=["usre"])
templates = Jinja2Templates(directory="templates")


@router.get("/register", tags=["user"], response_class=HTMLResponse)
def register(request: Request):
    context = {"title": "Registration"}
    return templates.TemplateResponse(
        request=request, name="register.html", context=context
    )


@router.get("/profile/{id}", tags=["user"], response_class=HTMLResponse)
async def profile(
    id: int,
    request: Request,
    session: SessionDep,
):
    context = {"title": "Profile"}
    try:
        current_user = await get_current_user(
            request.cookies.get("access_token"),
            session,
        )
        if current_user:
            context.update({"current_user": current_user})
    except HTTPException:
        pass

    user = service.get_user(id, session)
    if user:
        context.update({"user": user})

    return templates.TemplateResponse(
        request=request, name="profile.html", context=context
    )


@router.post("", tags=["user"], status_code=status.HTTP_201_CREATED)
def create_user(user_create: UserCreate, session: SessionDep) -> UserOut:

    return service.create_user(user_create, session)


@router.get("", tags=["user"])
def get_users(
    session: SessionDep,
    params: Params = Depends(),
) -> Page[UserOut]:
    # set_page(Page[UserOut])
    # set_params(Params(size=10))
    return service.get_users(session)


@router.get("/{user_id}", tags=["user"])
def get_user(user_id: int, session: SessionDep) -> UserOut:

    return service.get_user(user_id, session)


@router.put("/{user_id}", tags=["user"])
def update_user(
    user_id: int,
    update_user: UserUpdate,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> UserOut:

    return service.update_user(user_id, update_user, session)


@router.delete("/{user_id}", tags=["user"], status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, session: SessionDep):

    return service.delete_user(user_id, session)
