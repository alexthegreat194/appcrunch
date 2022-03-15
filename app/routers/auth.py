from datetime import datetime
from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel
from passlib.context import CryptContext

from app.models import User
from app.database import engine


pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

router = APIRouter(tags=['auth'])

# auth helpers

def verify_passoword(password, hashed_password):
    return pwd_context.verify(password, hashed_password)

def generate_password_hash(password):
    return pwd_context.hash(password)

# Schema
class UserInput(BaseModel):
    username: str
    password: str

class ReturnStatus(BaseModel):
    success: bool = True
    msg: Optional[str] = None

@router.post('/signup', response_model=ReturnStatus)
async def signup(input: UserInput):
    print(input.json())

    pw_hash = generate_password_hash(input.password)
    new_user = User(
        username=input.username,
        password_hash=pw_hash,
        created_at=datetime.now()
    )
    print(new_user)

    return ReturnStatus()