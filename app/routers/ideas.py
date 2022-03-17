from datetime import datetime
from pprint import pprint
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

from app.models import Idea, Upvote, User, Comment
from app.database import engine
from app.schema import ReturnStatus
from app.routers.auth import get_current_user

router = APIRouter(tags=['ideas'])

# class IdeaOut(Idea):
#     user: User
#     upvotes: list[Upvote]
#     comments: list[Upvote]

@router.get('/ideas', response_model=list[Idea], response_model_include={'comments'})
def get_all_ideas():
    ideas = []
    with Session(engine) as session:
        statement = select(Idea).options(selectinload(Idea.user))
        result = session.exec(statement).all()
        for idea in result:
            buffer = dict(idea)
            buffer['user'] = dict(idea.user).pop('_sa_instance_state')
            buffer['comments'] = list(idea.comments)
            buffer['upvotes'] = list(idea.upvotes)
            buffer.pop('_sa_instance_state')
            pprint(buffer)
            to_send = Idea(**buffer)
            ideas.append(to_send)
    pprint(ideas)
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

