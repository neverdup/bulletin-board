import sys, os
from dotenv import load_dotenv

load_dotenv()

from sqlalchemy import select

sys.path.append(os.path.dirname(__file__))

from typing import Annotated, List
from fastapi import Request, FastAPI, HTTPException, Depends, Query, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from database import get_db
from schemas import PostResponse, UserCreate, UserUpdate, UserResponse
import auth
import service
from models import User
from post.router import router as post_router
from post import service as post_service
from user import service as user_service

from fastapi_pagination import Page, add_pagination, Params, set_page, set_params
from fastapi_pagination.ext.sqlalchemy import paginate
import traceback


SessionDep = Annotated[Session, Depends(get_db)]
CurrentUserDep = Annotated[User, Depends(auth.get_current_user)]

app = FastAPI()

app.include_router(auth.router)
app.include_router(post_router)

add_pagination(app)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(
    request: Request,
    session: SessionDep,
    page: int | None = 1,
    size: int | None = 10,
    query: str | None = None,
):
    context = {"title": "Home"}
    try:
        user = await auth.get_current_user(request.cookies.get("access_token"), session)
        context.update({"user": user})
    except Exception as err:
        print(err)

    try:
        posts = post_service.get_posts(
            page=page,
            size=size,
            query=query,
        )
        context.update({"posts": posts})
    except Exception:
        print(traceback.format_exc())

    return templates.TemplateResponse(
        request=request, name="home.html", context=context
    )


@app.get("/register", tags=["user"], response_class=HTMLResponse)
def register(request: Request):
    context = {"title": "Registration"}
    return templates.TemplateResponse(
        request=request, name="register.html", context=context
    )


@app.get("/profile", tags=["user"], response_class=HTMLResponse)
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


@app.post("/user", tags=["user"], status_code=status.HTTP_201_CREATED)
def create_user(user_create: UserCreate, session: SessionDep) -> UserResponse:

    return user_service.create_user(user_create, session)


@app.get("/user", tags=["user"])
def get_users(
    session: SessionDep,
    params: Params = Depends(),
) -> Page[UserResponse]:
    # set_page(Page[UserResponse])
    # set_params(Params(size=10))
    return user_service.get_users(session)


@app.get("/user/{user_id}", tags=["user"])
def get_user(user_id: int, session: SessionDep) -> UserResponse:

    return user_service.get_users(user_id, session)


@app.put("/user/{user_id}", tags=["user"])
def update_user(
    user_id: int,
    update_user: UserUpdate,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> UserResponse:

    return user_service.update_user(user_id, update_user, session)


@app.delete("/user/{user_id}", tags=["user"], status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):

    return user_service.delete_user(user_id)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", reload=True)
