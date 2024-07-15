from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.post.models import PostDB
from src.post.schemas import PostsCreate
from src.user.models import UserDB
from src.user.schemas import UserRead


class PostsController:
    @staticmethod
    async def get_all_messages(db: AsyncSession):
        query = select(PostDB)
        message_list = await db.execute(query)
        return [message[0] for message in message_list.fetchall()]

    @staticmethod
    async def get_manager_all_messages(db: AsyncSession, manager_id: int):
        query = select(UserDB).where(UserDB.created_by == manager_id)
        user_list = await db.execute(query)
        user_ids = [user[0].id for user in user_list.fetchall()]
        user_ids.append(manager_id)

        query = select(PostDB).where(PostDB.user_id.in_(user_ids))
        message_list = await db.execute(query)
        return [message[0] for message in message_list.fetchall()]

    @staticmethod
    async def get_user_all_messages(db: AsyncSession, user_id: int):
        query = select(PostDB).where(PostDB.user_id == user_id)
        message_list = await db.execute(query)
        return [message[0] for message in message_list.fetchall()]

    @staticmethod
    async def create_message(db: AsyncSession, message: PostsCreate, current_user: UserRead):
        query = (
            insert(PostDB)
            .values(
                text=message.text,
                chat_id=message.chat_id,
                bot_token=message.bot_token,
                user_id=current_user.id
            ).returning(PostDB.id))

        message_id = await db.execute(query)
        await db.commit()

        query = select(PostDB).where(PostDB.id == message_id.scalar_one())
        result = await db.execute(query)
        created_message = result.scalar_one()

        return created_message
