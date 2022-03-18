from ast import Return
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from pydantic import BaseModel
from sqlalchemy.orm import selectinload

from app.models import CommentBase, User, CommentReadWithRel, Comment
from app.database import engine
from app.schema import ReturnStatus
from app.routers.auth import get_current_user

router = APIRouter(tags=['comments'])


@router.get('/comments', response_model=List[CommentReadWithRel])
def get_all_comments():
    with Session(engine) as session:
        statement = select(Comment).options(selectinload('*'))
        comments = session.exec(statement).all()
        return comments 

@router.get('/comments/{id}', response_model=CommentReadWithRel)
def get_comment_by_id(id: int):
    with Session(engine) as session:
        statement = select(Comment).where(Comment.id == id).options(selectinload('*'))
        comment = session.exec(statement).first()
        return comment

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

@router.put('/comments/{id}', response_model=ReturnStatus)
def edit_comments(id: int, data: CommentIn, user: User = Depends(get_current_user)):
    with Session(engine) as session:
        statement = select(Comment).where(Comment.id == id).options(selectinload('*'))
        comment = session.exec(statement).first()
        if not comment:
            return ReturnStatus(False, 'comment does not exits')
        if comment.user_id is not user.id:
            return ReturnStatus(False, 'user does not own comment')

        comment.content = data.content
        session.add(comment)
        session.commit()
        session.refresh(comment)

    return ReturnStatus()

@router.delete('/comments/{id}', response_model=ReturnStatus)
def delete_comments(id: int, user: User = Depends(get_current_user)):
    with Session(engine) as session:
        statement = select(Comment).where(Comment.id == id).options(selectinload('*'))
        comment = session.exec(statement).first()
        if not comment:
            return ReturnStatus(False, 'comment does not exits')
        if comment.user_id is not user.id:
            return ReturnStatus(False, 'user does not own comment')

        session.delete(comment)
        session.commit()

    return ReturnStatus()