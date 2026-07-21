from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from jose import jwt, JWTError

from database import get_db
from models import User
from config import settings, limiter
from schemas import CreateUserRequest, Token, RefreshTokenRequest
from celery_worker import send_verification_email

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

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

def create_refresh_token(email: str, user_id: str, role: str, expired_time: timedelta):
    expires = datetime.now(timezone.utc) + expired_time
    encode = {'sub': email, 'id': user_id, 'role': role, 'exp': expires, 'type': 'refresh'}
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    user_model = User(
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        email = create_user_request.email,
        phone_number = create_user_request.phone_number,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        role = 'user',
        is_active = True
    )

    send_verification_email.delay(user_model.email)

    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return user_model

@router.post('/token', response_model=Token)
@limiter.limit('5/minute')
async def login_for_access_token(request: Request, form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
    token = create_access_token(user.email, user.id, user.role, timedelta(minutes=20))
    refresh_token = create_refresh_token(user.email, user.id, user.role, timedelta(days=7))
    return {'access_token': token, 'refresh_token': refresh_token, 'token_type': 'bearer'}

@router.post('/refresh', response_model=Token)
async def refresh_access_token(request_data: RefreshTokenRequest):
    try:
        payload = jwt.decode(request_data.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get('type') != 'refresh':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid token type')

        email: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')

        if email is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')

        new_access_token = create_access_token(email, user_id, user_role, timedelta(minutes=20))
        new_refresh_token = create_refresh_token(email, user_id, user_role, timedelta(days=7))

        return {
            'access_token': new_access_token,
            'refresh_token': new_refresh_token,
            'token_type': 'bearer'
        }
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid or expired refresh token')