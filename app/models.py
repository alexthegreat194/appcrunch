from datetime import datetime
from typing import Optional
from pydantic import Field
from sqlmodel import SQLModel

# User
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password_hash: str 
    created_at: datetime

    email: Optional[str]
    bio: Optional[str]
    pronouns: Optional[str]
    website: Optional[str]


# Idea


# Comment
# Upvote