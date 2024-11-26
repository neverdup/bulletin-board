from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str

    class Config:
        from_attributes = True


class UserUpdate(UserBase):

    name: str | None = None
    email: EmailStr | None = None

    class Config:
        from_attributes = True


class UserOut(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ReplyBase(BaseModel):
    content: str


class ReplyCreate(ReplyBase):
    post_id: int


class ReplyUpdate(ReplyBase):
    pass


class ReplyOut(ReplyBase):
    id: int
    user: UserOut
    created_at: datetime
    updated_at: datetime


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    title: str | None = None
    content: str | None = None


class PostOut(PostBase):
    id: int
    user_id: int
    replys: list[ReplyOut]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
