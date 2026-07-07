from sqlalchemy import Column, Integer, String, Text,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer,primary_key=True,index=True)
    title =Column(String(200),nullable=False)
    content = Column(Text,nullable=False)
    created_at = Column(DateTime(timezone=True),server_default=func.now())

    comments = relationship("Comment",back_populates="post",cascade="all,delete-orphan")



class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer,primary_key=True,index=True)
    content = Column(Text,nullable=False)
    author = Column(String(100),nullable=False)
    post_id = Column(Integer,ForeignKey("posts.id"),nullable=False)

    post = relationship("Post",back_populates="comments")