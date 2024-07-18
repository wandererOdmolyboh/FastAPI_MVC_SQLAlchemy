from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class PostDB(Base):
    """
    The PostDB model represents a post in the database.

    Each post has an id, text, and owner_id. The id is the primary key, and the owner_id is a foreign key that references the id of the user who owns the post.

    The owner relationship provides a link to the UserDB model that owns the post.

    Attributes:
        id: The primary key of the post.
        text: The text content of the post.
        owner_id: The id of the user who owns the post.
        owner: The UserDB model that owns the post.
    """
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(255))
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("UserDB", back_populates="messages")
