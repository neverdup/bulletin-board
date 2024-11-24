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


from database import get_db, SessionDep
import auth
from models import User
from user.router import router as user_router
from post.router import router as post_router
from post import service as post_service
from user import service as user_service

from fastapi_pagination import Page, add_pagination, Params, set_page, set_params
from fastapi_pagination.ext.sqlalchemy import paginate
import traceback


app = FastAPI()

app.include_router(auth.router)
app.include_router(user_router)
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", reload=True)
