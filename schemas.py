from pydantic import BaseModel
from datetime import datetime
from typing import List


class CommentBase(BaseModel):
    content :str
    author:str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id:int
    post_id:int

    class Config:
        from_attributes = True

class PostBase(BaseModel):
    title:str
    content:str

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id:int
    created_at:datetime
    comments :List[Comment] =[]

    class Config:
        from_attributes = True



