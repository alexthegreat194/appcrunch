from fastapi import APIRouter
from sqlmodel import Session, select

from app.models import Idea, User
from app.database import engine

router = APIRouter(tags=['ideas'])


@router.get('/ideas', response_model=list[Idea])
def get_all_ideas():
    ideas = []
    with Session(engine) as session:
        statement = select(Idea)
        result = session.exec(statement).all()
        ideas = result
    return ideas 
