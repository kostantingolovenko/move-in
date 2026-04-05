from fastapi import APIRouter, Depends, HTTPException, status, Path
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Annotated, Optional

from models import User
from routers.auth import get_current_user, bcrypt_context
from schemas import UpdateProfileRequest, UpdatePasswordRequest, UpdatePhoneNumberRequest

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



@router.get('/{user_id}')
async def read_user_info(user: user_dependency, db: db_dependency, user_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')

    user_model = db.query(User).filter(User.id==user_id).first()
    return {
        "first_name": user_model.first_name,
        "last_name": user_model.last_name,
        "phone_number": user_model.phone_number
    }


@router.put('/update_profile/', status_code=status.HTTP_204_NO_CONTENT)
async def update_profile(user: user_dependency, db:db_dependency, update_profile_request: UpdateProfileRequest):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')

    user_model = db.query(User).filter(User.id==user.get('id')).first()
    if update_profile_request.first_name:
        user_model.first_name = update_profile_request.first_name
    if update_profile_request.last_name:
        user_model.last_name = update_profile_request.last_name
    if update_profile_request.phone_number:
        user_model.phone_number = update_profile_request.phone_number


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
