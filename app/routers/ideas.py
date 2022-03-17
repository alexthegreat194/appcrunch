from ast import Return
from datetime import datetime
from pprint import pprint
from typing import List
from fastapi import APIRouter, Depends
from pydantic import BaseModel
import sqlalchemy
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

from app.models import Idea, IdeaBase, Upvote, User, Comment, IdeaRead, IdeaReadWithRel
from app.database import engine
from app.schema import ReturnStatus
from app.routers.auth import get_current_user

router = APIRouter(tags=['ideas'])

@router.get('/ideas', response_model=List[IdeaReadWithRel])
def get_all_ideas():
    with Session(engine) as session:
        statement = select(Idea)
        results = session.exec(statement).all()
        return results

@router.get('/ideas/{id}', response_model=IdeaReadWithRel)
def get_idea_by_id(id: int):
    with Session(engine) as session:
        print('Statement')
        statement = sqlalchemy.select(Idea).where(Idea.id == id).options(selectinload('*'))
        print('Idea')
        idea = session.execute(statement).scalars().first()
        return idea

class IdeaNew(BaseModel):
    title: str
    description: str

@router.post('/ideas', response_model=ReturnStatus )
def create_idea(data: IdeaNew, user: User = Depends(get_current_user)):
    with Session(engine) as session:
        idea = Idea(
            title=data.title,
            description=data.description,
            created_at=datetime.now(),
            user_id=user.id
        )
        session.add(idea)
        session.commit()
    return ReturnStatus()

@router.put('/ideas/{idea_id}', response_model=ReturnStatus)
def edit_idea(idea_id: int, data: IdeaBase, user: User = Depends(get_current_user)):
    with Session(engine) as session:
        idea = session.get(Idea, idea_id)
        if not idea:
            return ReturnStatus(success=False, msg='idea does not exits')
        if idea.user_id is not user.id:
            return ReturnStatus(success=False, msg='user does not own idea')
        
        idea.title = data.title
        idea.description = data.description
        session.add(idea)
        session.commit()
        session.refresh(idea)
    
    return ReturnStatus()

@router.delete('/ideas/{idea_id}', response_model=ReturnStatus)
def delete_idea(idea_id: int, user: User = Depends(get_current_user)):
    with Session(engine) as session:
        idea = session.get(Idea, idea_id)
        if not idea:
            return ReturnStatus(success=False, msg='idea does not exits')
        if idea.user_id is not user.id:
            return ReturnStatus(success=False, msg='user does not own idea')

        session.delete(idea)
        session.commit()

    return ReturnStatus()