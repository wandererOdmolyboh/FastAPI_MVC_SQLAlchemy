from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class PostDB(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(255))
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("UserDB", back_populates="messages")
