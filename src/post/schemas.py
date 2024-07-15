from pydantic import BaseModel


class PostsCreate(BaseModel):
    text: str
    user_id: int


class Posts(BaseModel):
    id: int
    text: str
