from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter(tags=['auth'])

# Schema
class UserInput(BaseModel):
    username: str
    password: str

class ReturnStatus(BaseModel):
    success: bool = True
    msg: Optional[str] = None

@router.post('/signup', response_model=ReturnStatus)
def signup(input: UserInput):
    print(input)
    return ReturnStatus()