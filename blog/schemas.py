from pydantic import BaseModel, ConfigDict, EmailStr
from typing import List, Optional


class User(BaseModel):
    name: str
    email: str
    password: str
    model_config = ConfigDict(from_attributes=True)

class ShowUserForBlog(BaseModel):
    name: str
    email: str
    model_config = ConfigDict(from_attributes=True)

class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List['Blog'] = [] 
    model_config = ConfigDict(from_attributes=True)


class BlogBase(BaseModel):
    title: str
    body: str

class Blog(BlogBase):
    model_config = ConfigDict(from_attributes=True)

class ShowBlog(BaseModel):
    title: str
    body: str
    creator: ShowUserForBlog 
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None