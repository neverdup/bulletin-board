from fastapi import APIRouter, status, Depends, Request
from fastapi_pagination import Page, Params
from schemas import PostCreate, PostResponse, PostUpdate
from post import service
from typing import Annotated, List
from auth import CurrentUserDep, get_current_user
from fastapi.templating import Jinja2Templates
from post import service as post_service
from database import SessionDep


router = APIRouter(prefix="/post", tags=["post"])
templates = Jinja2Templates(directory="templates")


@router.get("/create-post")
async def create_post(
    request: Request,
    session: SessionDep,
):
    """
    post creation page
    """
    context = {"title": "Create Post"}

    try:
        user = await get_current_user(request.cookies.get("access_token"), session)
        context.update({"user": user})
    except Exception as err:
        print(err)

    return templates.TemplateResponse(
        request=request, name="create-post.html", context=context
    )


@router.get("/post-page/{id}")
async def post_page(
    id: int,
    request: Request,
    session: SessionDep,
):
    """
    post update page
    """
    context = {"title": "Update Post"}

    try:
        user = await get_current_user(request.cookies.get("access_token"), session)
        context.update({"user": user})
    except Exception as err:
        print(err)

    post = post_service.get_post(id)
    context.update({"post": post})

    return templates.TemplateResponse(
        request=request, name="update-post.html", context=context
    )


@router.post("", status_code=status.HTTP_201_CREATED)
def create_post(
    post_create: PostCreate,
    current_user: CurrentUserDep,
) -> PostResponse:

    post = service.create_post(user_id=current_user.id, post_create=post_create)
    return post


@router.get("")
def get_posts(
    params: Params = Depends(),
    query: str | None = None,
) -> Page[PostResponse]:

    posts = post_service.get_posts(
        page=params.page,
        size=params.size,
        query=query,
    )
    return posts


@router.get("/{id}")
def get_post(id: int) -> PostResponse:

    post = post_service.get_post(id)
    return post


@router.put("/{id}")
def update_post(
    id: int,
    update_post: PostUpdate,
    current_user: CurrentUserDep,
) -> PostResponse:

    post = post_service.update_post(
        id=id,
        update_post=update_post,
        current_user=current_user,
    )
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    current_user: CurrentUserDep,
):

    post_service.delete_post(id, current_user)
