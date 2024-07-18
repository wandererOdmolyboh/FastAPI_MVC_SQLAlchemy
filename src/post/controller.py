from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.post.models import PostDB
from src.post.schemas import PostsCreate
from src.user.schemas import UserRead


class PostsController:
    @staticmethod
    async def get_all_messages(db: AsyncSession):
        query = select(PostDB)
        try:
            message_list = await db.execute(query)
            return [message[0] for message in message_list.fetchall()]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    @staticmethod
    async def get_posts(db: AsyncSession, user_id: int):
        query = select(PostDB).where(PostDB.owner_id == user_id)
        try:
            result = await db.execute(query)
            return result.scalars().all()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    @staticmethod
    async def create_message(db: AsyncSession, message: PostsCreate, current_user: UserRead):

        try:
            db_post = PostDB(text=message.text, owner_id=current_user.id)
            db.add(db_post)
            await db.commit()
            await db.refresh(db_post)
            return db_post
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")