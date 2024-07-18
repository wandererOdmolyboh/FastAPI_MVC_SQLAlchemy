from starlette import status
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.oauth2 import get_current_user
from src.dependencies import get_async_session

from src.post import schemas
from src.post.schemas import PostsGet
from src.user.schemas import UserRead
from src.post.controller import PostsController

router = APIRouter(tags=["post"])
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
