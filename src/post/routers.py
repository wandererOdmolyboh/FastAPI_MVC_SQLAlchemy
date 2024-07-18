from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.auth.oauth2 import get_current_user
from src.dependencies import get_async_session
from src.post import schemas
from src.post.controller import PostsController
from src.post.schemas import PostsGet
from src.user.schemas import UserRead

router = APIRouter(tags=["post"])

#   AddPost Endpoint:
#     Accepts `text` and a `token` for authentication.
#     Validates payload size (limit to 1 MB), saves the post in memory, returning `postID`.
#     Returns an error for invalid or missing token.
#     Dependency injection for token authentication.
#   GetPosts Endpoint:
#     Requires a token for authentication.
#     Returns all user's posts.
#     Implements response caching for up to 5 minutes for the same user.
#     Returns an error for invalid or missing token.
#     Dependency injection for token authentication.
#
#   DeletePost Endpoint:
#     Accepts `postID` and a `token` for authentication.
#     Deletes the corresponding post from memory.
#     Returns an error for invalid or missing token.
#     Dependency injection for token authentication.

user_controller = PostsController()


@router.delete("/posts/{post_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
        post_id: int,
        current_user: UserRead = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_session)
):
    await user_controller.delete_post(db=db, post_id=post_id, user_id=current_user.id)


@router.get("/posts/", response_model=list[PostsGet])
async def get_messages(
        current_user: UserRead = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_session)
):
    messages = await user_controller.get_all_posts(db, current_user.id)
    return messages


@router.post("/posts/", status_code=status.HTTP_201_CREATED)
async def create_message(
        post: schemas.PostsCreate,
        current_user: UserRead = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_session)
):
    created_post_id = await user_controller.create_posts(db=db, post=post, current_user=current_user)

    return created_post_id
