from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.models import User
from app.database import engine

SECRET_KEY = 'df4a5e279fa58b9c45ac3e5ed35f63515ecd11d3b5f9549c4d098039ed72fab3'
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter(tags=['auth'])

# auth helpers

def verify_passoword(password, hashed_password):
    return pwd_context.verify(password, hashed_password)

def generate_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str):
    found_user = None
    with Session(engine) as session:
        statement = select(User).where(User.username == username)
        found_user = session.exec(statement).first()

    if not found_user:
        return False
    
    if not verify_passoword(password, found_user.password_hash):
        return False

    return True

def create_access_token(data: dict):
    # data would include a jwt that can be decrypted later with a secret key
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    # use when something goes wrong
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # get username from jwt
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['bcrypt'])
        username: str = payload.get('username') # make sure this is right later
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # find user in db
    with Session(engine) as session:
        statement = select(User).where(User.username == username)
        user = session.exec(statement).first()
    
    if user is None:
        raise credentials_exception

    return user


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

@router.post('/token', response_model=Token)
async def login_for_access_tokenken(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={'username': form_data.username}
    )
    return Token(access_token=access_token, token_type='bearer')

@router.post('/signup', response_model=ReturnStatus)
async def signup(input: UserInput):
    print(input.json())
    
    # see if data exists
    with Session(engine) as session:
        statement = select(User).where(User.username == input.username)
        result = session.exec(statement).first()
        print('query result:', result)
        if result:
            return ReturnStatus(success=False, msg='user exists')

    pw_hash = generate_password_hash(input.password)
    new_user = User(
        username=input.username,
        password_hash=pw_hash,
        created_at=datetime.now()
    )
    print(new_user)

    session = Session(engine)
    session.add(new_user)
    session.commit()

    return ReturnStatus()

@router.get('/test')
async def test(token: str = Depends(oauth2_scheme)):
    return {'test': True}