
from pydantic import BaseModel
from typing import Optional

# Schema
class Token(BaseModel):
    access_token: str
    token_type: str

class UserInput(BaseModel):
    username: str
    password: str

class ReturnStatus(BaseModel):
    success: bool = True
    msg: Optional[str] = None

