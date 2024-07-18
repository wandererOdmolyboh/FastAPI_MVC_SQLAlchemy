from pydantic import BaseModel, Field


class PostsCreate(BaseModel):
    text: str = Field(..., max_length=1024*1024)
    user_id: int


class PostsGet(BaseModel):
    owner_id: int
    text: str
