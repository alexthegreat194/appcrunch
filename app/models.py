from datetime import datetime
from typing import List, Optional
from sqlmodel import SQLModel, Relationship, Field

# User
class UserBase(SQLModel):
    username: str
    password_hash: str 
    created_at: datetime

    email: Optional[str]
    bio: Optional[str]
    pronouns: Optional[str]
    website: Optional[str]
    full_name: Optional[str]

class User(UserBase, table=True):
    __tablename__ = 'user'
    id: Optional[int] = Field(default=None, primary_key=True)

    ideas: List["Idea"] = Relationship(back_populates='user')
    comments: List["Comment"] = Relationship(back_populates='user')
    upvotes: List["Upvote"] = Relationship(back_populates='user')

class UserRead(UserBase):
    id: int

class kklko(UserRead):
    ideas: List['Idea'] = []
    comments: List["Comment"] = []
    upvotes: List["Upvote"] = []


# Idea
class IdeaBase(SQLModel):
    title: str
    description: str 
    created_at: datetime 

    user_id: int = Field(default=None, foreign_key='user.id')

class Idea(IdeaBase, table=True):
    __tablename__ = 'idea'
    id: Optional[int] = Field(default=None, primary_key=True)

    user: User = Relationship(back_populates='ideas')
    upvotes: List['Upvote'] = Relationship(back_populates='idea')
    comments: List['Comment'] = Relationship(back_populates='idea')

class IdeaRead(IdeaBase):
    id: int

class IdeaReadWithRel(IdeaBase):
    user: Optional[User] = None
    upvotes: List['Upvote'] = []
    comments: List['Comment'] = []


# Comment
class CommentBase(SQLModel):
    content: str 
    created_at: datetime

    user_id: int = Field(default=None, foreign_key='user.id')
    idea_id: int = Field(default=None, foreign_key='idea.id')
    reply_id: Optional[int] = Field(default=None, foreign_key='comment.id')

class Comment(CommentBase, table=True):
    __tablename__ = 'comment'
    id: Optional[int] = Field(default=None, primary_key=True)

    user: User = Relationship(back_populates='comments')
    idea: Idea = Relationship(back_populates='comments')

class CommentRead(CommentBase):
    id: str

class CommentReadWithRel(CommentRead):
    user: User
    idea: Idea

# Upvote
class UpvoteBase(SQLModel):
    created_at: datetime

class Upvote(UpvoteBase, table=True):
    __tablename__ = 'upvote'
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(default=None, foreign_key='user.id')
    idea_id: int = Field(default=None, foreign_key='idea.id')

    user: User = Relationship(back_populates='upvotes')
    idea: Idea = Relationship(back_populates='upvotes')

class UpvoteRead(UpvoteBase):
    id: int

class UpvoteReadWithRel(UpvoteRead):
    user: User
    idea: Idea 