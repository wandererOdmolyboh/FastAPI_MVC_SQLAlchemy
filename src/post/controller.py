import aiocache
from starlette import status
from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import TIME_EXPIRE
from src.post.models import PostDB
from src.user.schemas import UserRead
from src.post.schemas import PostsCreate


class PostsController:
    @staticmethod
    async def delete_post(db: AsyncSession, post_id: int, user_id: int):
        query = select(PostDB).where(PostDB.id == post_id, PostDB.owner_id == user_id)
        try:
            result = await db.execute(query)
            post = result.scalar_one_or_none()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"An error occurred: {str(e)}")

        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        try:
            await db.delete(post)
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"An error occurred: {str(e)}")

    @staticmethod
    @aiocache.cached(ttl=TIME_EXPIRE)
    async def get_all_posts(db: AsyncSession, user_id: int):
        query = select(PostDB).where(PostDB.owner_id == user_id)
        try:
            result = await db.execute(query)
            return result.scalars().all()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"An error occurred: {str(e)}")

    @staticmethod
    async def get_posts(db: AsyncSession, user_id: int):
        query = select(PostDB).where(PostDB.owner_id == user_id)
        try:
            result = await db.execute(query)
            return result.scalars().all()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"An error occurred: {str(e)}")

    @staticmethod
    async def create_posts(db: AsyncSession, post: PostsCreate, current_user: UserRead):

        try:
            db_post = PostDB(text=post.text, owner_id=current_user.id)
            db.add(db_post)
            await db.commit()
            await db.refresh(db_post)
            return db_post.id
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"An error occurred: {str(e)}")
