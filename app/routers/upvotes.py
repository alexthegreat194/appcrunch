
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

from app.models import Idea, Upvote, UpvoteReadWithRel, User
from app.routers.auth import get_current_user
from app.schema import ReturnStatus
from app.database import engine

router = APIRouter(tags=['upvotes'])

@router.get('/upvotes', response_model=List[UpvoteReadWithRel])
def get_all_upvotes():
    with Session(engine) as session:
        return session.exec(select(Upvote).options(selectinload('*'))).all()


@router.post('/upvotes/upvote/{idea_id}', response_model=ReturnStatus)
def upvote_idea_by_id(idea_id: int, downvote: Optional[bool] = False, user: User = Depends(get_current_user)):
    with Session(engine) as session: 
        idea = session.exec(select(Idea).where(Idea.id == idea_id)).first()
        if not idea:
            return ReturnStatus(False, 'idea does not exist')
        
        found_upvote = session.exec(select(Upvote).where(Upvote.user_id == user.id and Upvote.idea_id == idea.id)).first()
        if found_upvote:
            if downvote:
                session.delete(found_upvote)
                session.commit()
            else:
                return ReturnStatus(success=False, msg='upvote already exists')
        else:
            if downvote:
                return ReturnStatus(success=False, msg='upvote does not exist')
            else:
                upvote = Upvote(
                    created_at=datetime.now(),
                    user_id=user.id,
                    idea_id=idea.id
                )
                session.add(upvote)
                session.commit()

    return ReturnStatus()