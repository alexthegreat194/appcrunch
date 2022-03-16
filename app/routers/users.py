from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
import sqlalchemy
from sqlmodel import Session
from sqlalchemy import select
from jose import JWTError, jwt

from app.models import User
from app.database import engine
from app.routers.auth import ReturnStatus, oauth2_scheme, get_current_user

router = APIRouter(tags=['Users'])

SECRET_KEY = 'df4a5e279fa58b9c45ac3e5ed35f63515ecd11d3b5f9549c4d098039ed72fab3'
ALGORITHM = "HS256"


@router.get('/users', response_model=list[User], response_model_exclude={'password_hash'})
def get_users(limit: Optional[int] = None):
    users: list[User] = []
    with Session(engine) as session:
        for user in session.query(User):
            if limit:
                if len(users) >= limit:
                    break
            users.append(user)
            print('User:', user.username)
    print('----before----:', users)
    return users
        

@router.get('/users/{username}', response_model=User, response_model_exclude={'password_hash'})
def get_user_by_username(username: str):
    with Session(engine) as session:
        statement = select(User).select_from(User).where(User.username == username)
        result = session.exec(statement).first()
        return result 

@router.get('/users/{user_id}', response_model=User, response_model_exclude={'password_hash'})
def get_user_by_id(user_id: int):
    print('\n')
    print('this is the result: -')
    print('\n')
    with Session(engine) as session:
        statement = sqlalchemy.select(User).where(User.id == user_id)
        result = session.exec(statement).first()
        print('\n')
        print('this is the result: -', result)
        print('\n')
    return result 

class UserIn(BaseModel):
    email: Optional[str]
    bio: Optional[str]
    pronouns: Optional[str]
    website: Optional[str]
    full_name: Optional[str]


@router.put('/users', response_model=ReturnStatus)
def change_user_data(data: UserIn, user: User = Depends(get_current_user)):
    print('-----')
    print(data.json(), user.json())
    with Session(engine) as session:
        user.email = data.email
        user.bio = data.bio
        user.pronouns = data.pronouns
        user.full_name = data.full_name
        user.website = data.website

        session.add(user)
        session.commit()
        session.refresh(user)

    return ReturnStatus()