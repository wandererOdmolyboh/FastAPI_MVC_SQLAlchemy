from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from enum import StrEnum

from sqlalchemy.orm import relationship

from src.database import Base
from src.post.models import PostDB
from src.user.constant import ENUM_MALE, ENUM_FEMALE


class SexEnum(StrEnum):
    """
    The SexEnum class is an enumeration of the possible sexes a user can have.

    The possible values are MALE and FEMALE.

    Attributes:
        MALE: Represents a male user.
        FEMALE: Represents a female user.
    """
    MALE = ENUM_MALE
    FEMALE = ENUM_FEMALE


class UserDB(Base):
    """
    The UserDB class represents a user in the database.

    Each user has an id, username, email, sex, and password. The id is the primary key. The username and email are unique. The sex is an enumeration of the possible sexes a user can have.

    The messages relationship provides a link to the PostDB models that the user owns.

    Attributes:
        id: The primary key of the user.
        username: The username of the user.
        email: The email of the user.
        sex: The sex of the user.
        password: The password of the user.
        messages: The posts that the user owns.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True)
    email = Column(String(255), unique=True, index=True)
    sex = Column(Enum(SexEnum), nullable=False)
    password = Column(String(255))

    messages = relationship("PostDB", back_populates="owner")
