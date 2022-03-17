from datetime import datetime
from pprint import pprint
from typing import List
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

from app.models import Idea, Upvote, User, Comment, IdeaRead, IdeaReadWithRel
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

