from pydantic import BaseModel, Field

from src.config import MAX_LENGTH


class PostsCreate(BaseModel):
    """
    The PostsCreate model represents a post that is being created.

    Each PostsCreate object has a text and a user_id. The text is the content of the post, and the user_id is the id of the user who is creating the post.

    Attributes:
        text: The text content of the post.
        user_id: The id of the user who is creating the post.
    """

    text: str = Field(..., max_length=MAX_LENGTH)
    user_id: int

    class Config:
        from_attributes = True


class PostsGet(BaseModel):
    """
    The PostsGet model represents a post that is being retrieved.

    Each PostsGet object has an owner_id and a text. The owner_id is the id of the user who owns the post, and the text is the content of the post.

    Attributes:
        owner_id: The id of the user who owns the post.
        text: The text content of the post.
    """
    owner_id: int
    text: str

    class Config:
        from_attributes = True
