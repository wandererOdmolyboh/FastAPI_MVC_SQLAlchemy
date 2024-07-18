from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.auth.oauth2 import get_current_user
from src.user.controller import UserController
from src.user.schemas import UserRead, UserCreate
from src.dependencies import get_async_session

router = APIRouter(tags=["users"])
user_controller = UserController()


@router.get("/users/", response_model=list[UserRead])
async def get_all_users(
        current_user: UserRead = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_session)
):
    return await user_controller.get_users_list(db_session=db)


@router.get("/users/{user_id}/", response_model=UserRead)
async def user_detail(
        user_id: int,
        current_user: UserRead = Depends(get_current_user),
        db_session: AsyncSession = Depends(get_async_session)):

    db_user = await user_controller.get_user_detail_by_id(db_session=db_session, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return db_user
