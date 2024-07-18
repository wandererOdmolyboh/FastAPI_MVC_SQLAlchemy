import aiocache
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.post.models import PostDB
from src.post.schemas import PostsCreate
from src.user.schemas import UserRead


class PostsController:
    @staticmethod
    async def delete_post(db: AsyncSession, post_id: int, user_id: int):
        query = select(PostDB).where(PostDB.id == post_id, PostDB.owner_id == user_id)
        result = await db.execute(query)
        post = result.scalar_one_or_none()

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        await db.delete(post)
        await db.commit()

    @staticmethod
    @aiocache.cached(ttl=300)
    async def get_all_posts(db: AsyncSession, user_id: int):
        query = select(PostDB).where(PostDB.owner_id == user_id)
        try:
            result = await db.execute(query)
            return result.scalars().all()
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
    async def create_posts(db: AsyncSession, post: PostsCreate, current_user: UserRead):

        try:
            db_post = PostDB(text=post.text, owner_id=current_user.id)
            db.add(db_post)
            await db.commit()
            await db.refresh(db_post)
            return db_post.id
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")