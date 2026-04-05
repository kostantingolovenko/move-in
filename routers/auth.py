from http.client import HTTPException
from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from jose import jwt, JWTError

from database import SessionLocal
from models import User
from config import settings
from schemas import CreateUserRequest, Token

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')



async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if email is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
        return {'email': email, 'id': user_id, 'role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')

def authenticate_user(email: str, password: str, db):
    user_model = db.query(User).filter(User.email==email).first()
    if not user_model:
        return False
    if not bcrypt_context.verify(password, user_model.hashed_password):
        return False
    return user_model

def create_access_token(email: str, user_id: str, role: str, expired_time: timedelta):
    expires = datetime.now(timezone.utc) + expired_time
    encode = {'sub': email, 'id': user_id, 'role': role, 'exp': expires}
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    user_model = User(
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        email = create_user_request.email,
        phone_number = create_user_request.phone_number,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        role = create_user_request.role,
        is_active = True
    )
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return user_model

@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
    token = create_access_token(user.email, user.id, user.role, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}