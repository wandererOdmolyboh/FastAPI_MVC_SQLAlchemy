from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.utils import hash_password
from src.user.models import SexEnum
from src.user.schemas import UserCreate
from src.user.controller import UserController

user_controller = UserController()


def test_set_user():
    return [
        {
            "username": "Sergey",
            "email": "sergey@test.com",
            "password": hash_password("admin"),
            "sex": SexEnum.MALE,
        },
        {
            "username": "Pusha",
            "email": "pusha@test.com",
            "password": hash_password("user"),
            "sex": SexEnum.FEMALE,
        },
    ]


async def create_test_users(db: AsyncSession):
    test_users = [UserCreate(**user) for user in test_set_user()]

    for user in test_users:
        await user_controller.create_user(db, user_create=user)
