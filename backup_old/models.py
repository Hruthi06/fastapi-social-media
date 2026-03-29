from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class PostOut(Post):
    id: int
    created_at: datetime
    owner_id: int
    owner_email: str

    class Config:
        orm_mode = True
