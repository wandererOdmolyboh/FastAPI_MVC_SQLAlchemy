from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, JWT_SECRET
from src.dependencies import get_async_session
from src.user.controller import UserController

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/task_2/login", auto_error=False)
user_controller = UserController()


def create_access_token(
        payload: dict,
        expires_delta: Optional[timedelta] = None
):
    """
    Create a new access token.

    :param payload: The payload to encode into the token. This should include any information you want to carry in the token, such as the user's ID.
    :param expires_delta: The amount of time until the token expires. If not provided, defaults to ACCESS_TOKEN_EXPIRE_MINUTES.
    :return: The encoded JWT as a string.
    """

    to_encode = payload.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(payload=to_encode, key=JWT_SECRET, algorithm=ALGORITHM)

    return encoded_jwt


async def get_current_user(
        token: str = Depends(oauth2_schema),
        db: AsyncSession = Depends(get_async_session)
):
    """
    Get the current logged-in user.

    :param token: The JWT token for the user.
    :param db: The database session.
    :return: The User object for the current user.
    :raise HTTPException: If the user is not found.
    """
    user_id = await validate_token(token)
    if user_id is None:
        raise_unauthorized_exception()
    else:
        user = await user_controller.get_user_detail_by_id(db, user_id=user_id)
        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        return user


async def validate_token(token) -> int | None:
    """
    Validate a JWT token and return the user's ID.

    :param token: The JWT token to validate.
    :return: The user's ID if the token is valid, None otherwise.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        user_id = int(payload.get("user_id"))
        return user_id
    except jwt.PyJWTError:
        return None


def raise_unauthorized_exception():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
