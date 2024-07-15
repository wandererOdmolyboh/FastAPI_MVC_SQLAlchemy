from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from enum import StrEnum

from sqlalchemy.orm import relationship

from src.database import Base
from src.post.models import PostDB
from src.user.constant import ENUM_MALE, ENUM_FEMALE


class SexEnum(StrEnum):
    MALE = ENUM_MALE
    FEMALE = ENUM_FEMALE


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True)
    email = Column(String(255), unique=True, index=True)
    sex = Column(Enum(SexEnum), nullable=False)
    password = Column(String(255))

    messages = relationship("PostDB", back_populates="owner")
