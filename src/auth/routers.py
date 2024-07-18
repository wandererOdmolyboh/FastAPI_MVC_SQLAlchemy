from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.auth.oauth2 import create_access_token
from src.auth.utils import verify_password
from src.dependencies import get_async_session
from src.user.controller import UserController

user_controller = UserController()
router = APIRouter(tags=["authentication"])


#   Signup Endpoint:
#     Accepts `email` and `password`.
#     Returns a token (JWT or randomly generated string).
#
#
#   Login Endpoint:
#     Accepts `email` and `password`.
#     Returns a token upon successful login; error response if login fails.
@router.post("/login")
async def get_token(
        request: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(get_async_session)
):
    """
    Authenticate a user and generate an access token for them.

    The user must provide their username and password. If the username and password are correct, an access token is generated and returned.

    Args:
        request (OAuth2PasswordRequestForm): The request object, which contains the username and password provided by the user.
        session (AsyncSession): The database session.

    Returns:
        dict: A dictionary containing the access token, the token type, and the user's ID.

    Raises:
        HTTPException: If the user is not found or the password is incorrect.
    """
    user = await user_controller.get_user_detail_by_name(
        db_session=session,
        username=request.username
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if not verify_password(
            plain_password=request.password,
            hashed_password=user.password
    ):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")

    access_token = create_access_token(payload={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer", "user": user.id}
