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


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    title: str | None = None
    content: str | None = None


class PostResponse(PostBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
