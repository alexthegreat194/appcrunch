from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from pydantic import BaseModel

from app.models import CommentBase, User, CommentReadWithRel, Comment
from app.database import engine
from app.schema import ReturnStatus
from app.routers.auth import get_current_user

router = APIRouter(tags=['comments'])


@router.get('/comments', response_model=List[CommentReadWithRel])
def get_all_comments():
    with Session(engine) as session:
        statement = select(Comment)
        comments = session.exec(statement).all()
        return comments 

class CommentIn(BaseModel):
    content: str
    idea_id: int
    reply_id: Optional[int] = None


@router.post('/comments', response_model=ReturnStatus)
def create_comment(data: CommentIn, user: User = Depends(get_current_user)):
    with Session(engine) as session:
        comment = Comment(
            content=data.content,
            created_at=datetime.now(),
            user_id=user.id,
            idea_id=data.idea_id,
            reply_id=data.reply_id
        )

        session.add(comment)
        session.commit()

    return ReturnStatus()