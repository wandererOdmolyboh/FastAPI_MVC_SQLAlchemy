from fastapi import HTTPException

from starlette import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.user.schemas import UserCreate
from src.user.models import UserDB, SexEnum


class UserController:
    @staticmethod
    async def get_users_list(
            db_session: AsyncSession,
            sex: SexEnum | None = None
    ):
        query = select(UserDB)
        if sex is not None:
            query = query.where(UserDB.sex == sex)

        try:
            user_list = await db_session.execute(query)
            return user_list.scalars().all()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"An error occurred: {str(e)}")

    @staticmethod
    async def create_user(db_session: AsyncSession, user_create: UserCreate):

        try:
            db_user = UserDB(**user_create.dict())
            db_session.add(db_user)
            await db_session.commit()
            await db_session.refresh(db_user)
            return db_user
        except Exception as e:
            await db_session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"An error occurred: {str(e)}")

    @staticmethod
    async def get_user_detail_by_name(db_session: AsyncSession, username: str):
        query = select(UserDB).where(UserDB.username == username)
        try:
            result = await db_session.execute(query)
            return result.scalar_one_or_none()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"An error occurred: {str(e)}")

    @staticmethod
    async def get_user_detail_by_id(db_session: AsyncSession, user_id: int):
        query = select(UserDB).where(UserDB.id == user_id)
        try:
            result = await db_session.execute(query)
            return result.scalar_one_or_none()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"An error occurred: {str(e)}")
