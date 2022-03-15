from datetime import datetime
from typing import List, Optional
from sqlmodel import SQLModel, Relationship, Field

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
    full_name: Optional[str]

    ideas: List["Idea"] = Relationship(back_populates='user')
    comments: List["Comment"] = Relationship(back_populates='user')
    upvotes: List["Upvote"] = Relationship(back_populates='user')

# Idea
class Idea(SQLModel, table=True):
    __tablename__ = 'idea'

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str 
    created_at: datetime 

    user_id: int = Field(default=None, foreign_key='user.id')
    user: User = Relationship(back_populates='ideas')

    upvotes: List["Upvote"] = Relationship(back_populates='idea')


# Comment
class Comment(SQLModel, table=True):
    __tablename__ = 'comment'

    id: Optional[int] = Field(default=None, primary_key=True)
    content: str 
    created_at: datetime

    user_id: int = Field(default=None, foreign_key='user.id')
    user: User = Relationship(back_populates='comments')

    idea_id: int = Field(default=None, foreign_key='idea.id')
    idea: User = Relationship(back_populates='comments')

    reply_id: Optional[int] = Field(default=None, foreign_key='comment.id')


# Upvote
class Upvote(SQLModel, table=True):
    __tablename__ = 'upvote'

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime

    user_id: int = Field(default=None, foreign_key='user.id')
    user: User = Relationship(back_populates='upvotes')

    idea_id: int = Field(default=None, foreign_key='idea.id')
    idea: Idea = Relationship(back_populates='upvotes')

