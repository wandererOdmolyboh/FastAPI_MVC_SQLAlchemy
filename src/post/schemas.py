from pydantic import BaseModel


class PostsCreate(BaseModel):
    text: str
    user_id: int


class PostsGet(BaseModel):
    owner_id: int
    text: str
