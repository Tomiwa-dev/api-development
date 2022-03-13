from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic.types import conint
# for structuring inputs and responses. so user can't enter what they like


class User(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserResponse(BaseModel):
    email: EmailStr
    username: str
    id: int

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Post(BaseModel):
    title: str
    content: str
    publish: bool = True


class PostCreate(Post):
    pass


class PostResponse(Post):
    id: int
    timestamp: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int

class Votes(BaseModel):
    post_id: int
    dir: conint(le=1)

class VoteResponse(BaseModel):
    Posts: PostResponse
    votes: int

    class Config:
        orm_mode = True