from fastapi import APIRouter, Depends, HTTPException, status, Path
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Annotated, Optional

from models import User
from routers.auth import get_current_user, bcrypt_context

router = APIRouter(
    prefix='/user',
    tags=['user']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class UpdatePasswordRequest(BaseModel):
    old_password: str
    new_password: str

class UpdatePhoneNumberRequest(BaseModel):
    new_phone_number: str

@router.get('/{user_id}')
async def read_user_info(user: user_dependency, db: db_dependency, user_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')

    user_model = db.query(User).filter(User.id==user_id).first()
    info = {
        user_model.first_name,
        user_model.last_name,
        user_model.phone_number
    }
    return info

@router.put('/update_profile/', status_code=status.HTTP_204_NO_CONTENT)
async def update_profile(user: user_dependency, db:db_dependency,
                         first_name: Optional[str] = None,
                         last_name: Optional[str] = None,
                         phone_number: Optional[str] = None):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')

    user_model = db.query(User).filter(User.id==user.get('id')).first()
    if first_name:
        user_model.first_name = first_name
    if last_name:
        user_model.last_name = last_name
    if phone_number:
        user_model.phone_number = phone_number


    db.add(user_model)
    db.commit()

@router.put('/change_password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, update_pass_request: UpdatePasswordRequest):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')

    user_model = db.query(User).filter(User.id==user.get('id')).first()
    if bcrypt_context.verify(update_pass_request.old_password, user_model.hashed_password):
        user_model.hashed_password = bcrypt_context.hash(update_pass_request.new_password)

    db.add(user_model)
    db.commit()

@router.put('/change_phone_number', status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user: user_dependency, db: db_dependency,
                              update_phone_request: UpdatePhoneNumberRequest):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')

    user_model = db.query(User).filter(User.id==user.get('id')).first()
    user_model.phone_number = update_phone_request.new_phone_number

    db.add(user_model)
    db.commit()
