from pydantic import BaseModel, Field

from src.config import MAX_LENGTH


class PostsCreate(BaseModel):
    text: str = Field(..., max_length=MAX_LENGTH)
    user_id: int

    class Config:
        from_attributes = True


class PostsGet(BaseModel):
    owner_id: int
    text: str

    class Config:
        from_attributes = True
