from pydantic import BaseModel, field_validator

from src.user.models import SexEnum
from src.auth.utils import hash_password


class UserCreate(BaseModel):
    """
    The UserCreate model represents the data required to create a new user.

    Each UserCreate object has a username, email, sex, and password. The username and email are the unique identifiers of the user. The sex is one of the values defined in the SexEnum class. The password is the user's password.

    Attributes:
        username: The username of the user.
        email: The email address of the user.
        sex: The sex of the user. This must be one of the values defined in the SexEnum class.
        password: The password of the user.
    """

    username: str
    email: str
    sex: SexEnum
    password: str

    @field_validator('password')
    @staticmethod
    def hash_password(password):
        return hash_password(password)

    class Config:
        """
        A nested class for Pydantic model configuration. The 'from_attributes' attribute is set to True, which means
        that attributes of the model instance will be used to populate the dictionary when the model is converted to a
        dictionary using the 'dict()' function.
        """
        from_attributes = True


class UserRead(BaseModel):
    """
    The UserRead model represents the data of a user that is being retrieved.

    Each UserRead object has a username, sex, and id. The username is the unique identifier of the user. The sex is one of the values defined in the SexEnum class. The id is the unique identifier of the user in the database.

    Attributes:
        username: The username of the user.
        sex: The sex of the user. This must be one of the values defined in the SexEnum class.
        id: The unique identifier of the user in the database.
    """

    username: str
    sex: SexEnum
    id: int

    class Config:
        """
        A nested class for Pydantic model configuration. The 'from_attributes' attribute is set to True, which means
        that attributes of the model instance will be used to populate the dictionary when the model is converted to a
        dictionary using the 'dict()' function.
        """
        from_attributes = True
