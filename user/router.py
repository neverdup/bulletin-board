from typing import Annotated
from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_pagination import Page, Params
from sqlalchemy.orm import Session

import auth
from database import get_db
from models import User
from schemas import UserCreate, UserResponse, UserUpdate
from user import service

router = APIRouter(prefix="/user", tags=["usre"])
templates = Jinja2Templates(directory="templates")

SessionDep = Annotated[Session, Depends(get_db)]
CurrentUserDep = Annotated[User, Depends(auth.get_current_user)]


@router.get("/register", tags=["user"], response_class=HTMLResponse)
def register(request: Request):
    context = {"title": "Registration"}
    return templates.TemplateResponse(
        request=request, name="register.html", context=context
    )


@router.get("/profile", tags=["user"], response_class=HTMLResponse)
async def profile(
    request: Request,
    session: SessionDep,
):
    context = {"title": "Profile"}
    current_user = await auth.get_current_user(
        request.cookies.get("access_token"),
        session,
    )
    if current_user:
        context.update({"user": current_user})

    return templates.TemplateResponse(
        request=request, name="profile.html", context=context
    )


@router.post("", tags=["user"], status_code=status.HTTP_201_CREATED)
def create_user(user_create: UserCreate, session: SessionDep) -> UserResponse:

    return service.create_user(user_create, session)


@router.get("", tags=["user"])
def get_users(
    session: SessionDep,
    params: Params = Depends(),
) -> Page[UserResponse]:
    # set_page(Page[UserResponse])
    # set_params(Params(size=10))
    return service.get_users(session)


@router.get("/{user_id}", tags=["user"])
def get_user(user_id: int, session: SessionDep) -> UserResponse:

    return service.get_users(user_id, session)


@router.put("/{user_id}", tags=["user"])
def update_user(
    user_id: int,
    update_user: UserUpdate,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> UserResponse:

    return service.update_user(user_id, update_user, session)


@router.delete("/{user_id}", tags=["user"], status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):

    return service.delete_user(user_id)
