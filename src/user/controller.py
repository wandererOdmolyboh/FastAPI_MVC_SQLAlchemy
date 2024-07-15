from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.user.models import UserDB, SexEnum
from src.user.schemas import UserCreate


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
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    @staticmethod
    async def create_user(
            db_session: AsyncSession,
            user_create: UserCreate):

        query = insert(UserDB).values(
            **user_create.model_dump()
        )

        try:
            await db_session.execute(query)
            await db_session.commit()

            return user_create

        except Exception as e:
            await db_session.rollback()
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    @staticmethod
    async def get_user_detail(db_session: AsyncSession, username: str):
        query = select(UserDB).where(UserDB.username == username)
        try:
            result = await db_session.execute(query)
            return result.scalar_one_or_none()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
