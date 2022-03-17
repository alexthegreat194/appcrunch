from datetime import datetime
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session, select

from app.models import Idea, User
from app.database import engine
from app.schema import ReturnStatus
from app.routers.auth import get_current_user

router = APIRouter(tags=['ideas'])


@router.get('/ideas', response_model=list[Idea])
def get_all_ideas():
    ideas = []
    with Session(engine) as session:
        statement = select(Idea)
        result = session.exec(statement).all()
        ideas = result
    return ideas 

class IdeaNew(BaseModel):
    title: str
    description: str

@router.post('/ideas', response_model=ReturnStatus, )
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