from datetime import datetime
from sqlalchemy import String, Column, Integer, TIMESTAMP, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "user"
    id: int = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name: str = Column(String(32), nullable=False)
    email: str = Column(String(100), nullable=False, unique=True)
    password: str = Column(String, nullable=False)
    created_at: datetime = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: datetime = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    posts = relationship("Post", back_populates="user")

    def __str__(self):
        return f"User(email='{self.email}')"


class Post(Base):
    __tablename__ = "post"
    id: int = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id: int = Column(Integer, ForeignKey("user.id"))
    title: str = Column(String(200), nullable=False)
    content: Text = Column(Text, nullable=False)
    created_at: datetime = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: datetime = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    user = relationship("User", back_populates="posts")

    def __str__(self):
        return f"Post(title='{self.title}')"
