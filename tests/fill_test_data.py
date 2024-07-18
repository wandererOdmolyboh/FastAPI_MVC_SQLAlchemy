import asyncio

from src.database import SessionLocal
from tests.dumps.dumps_account import create_test_users


async def main():
    async with SessionLocal() as db_session:
        await create_test_users(db_session)

asyncio.run(main())
