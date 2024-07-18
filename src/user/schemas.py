from pydantic import BaseModel, field_validator

from src.user.models import SexEnum
from src.auth.utils import hash_password


class UserCreate(BaseModel):
    """
    A Pydantic model that defines the data required to create a new user. This model inherits all fields from UserBase,
    and adds a field for the user's password.

    Args:
        username (str): The username of the user.
        email (str): The email address of the user.
        sex (SexEnum): The sex of the user. This must be one of the values defined in the SexEnum class.
        password (str): The password of the user.
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
