from datetime import datetime
from typing import Optional
from pydantic import Field
from sqlalchemy import table
from sqlmodel import SQLModel

# User
class User(SQLModel, table=True):
    __tablename__ = 'user'

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password_hash: str 
    created_at: datetime

    email: Optional[str]
    bio: Optional[str]
    pronouns: Optional[str]
    website: Optional[str]


# Idea
class Idea(SQLModel, table=True):
    __tablename__ = 'idea'

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str 
    created_at: datetime 

    user_id: int = Field(default=None, foreign_key='user.id')

# Comment
class Comment(SQLModel, table=True):
    __tablename__ = 'comment'

    id: Optional[int] = Field(default=None, primary_key=True)
    content: str 
    created_at: datetime

    user_id: int = Field(default=None, foriegn_key='user.id')
    idea_id: int = Field(default=None, foriegn_key='idea.id')
    reply_id: int = Field(default=None, foriegn_key='comment.id')

# Upvote