from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session

from typing import Annotated, Optional, List

from models import User, Listings, Reviews
from routers.auth import get_current_user
from database import get_db
from schemas import UserResponse

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get('/', response_model=List[UserResponse])
async def read_all_users(user: user_dependency, db: db_dependency):
    if not user or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')

    return db.query(User).all()

@router.get('/{user_id}', response_model=UserResponse)
async def read_user_info(user: user_dependency, db:db_dependency, user_id: int=Path(gt=0)):
    if not user or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')

    return db.query(User).filter(User.id==user_id).first()

@router.put('/{user_id}/role')
async def grant_rights(user: user_dependency, db:db_dependency, user_id: int=Path(gt=0)):
    if not user or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')

    user_model = db.query(User).filter(User.id==user_id).first()
    user_model.role = 'admin'

    db.add(user_model)
    db.commit()
    return {'detail': 'Admin rights granted'}

@router.delete('/delete_listing/{listing_id}')
async def delete_listing(user: user_dependency, db: db_dependency, listing_id: int=Path(gt=0)):
    if not user or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')

    listing_model = db.query(Listings).filter(Listings.id==listing_id).first()
    if listing_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    db.query(Listings).filter(Listings.id==listing_id).delete()
    db.commit()

@router.delete('/delete_review/{review_id}')
async def delete_review(user: user_dependency, db: db_dependency, review_id: int = Path(gt=0)):
    if not user or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')

    review_model = db.query(Reviews).filter(Reviews.id == review_id).first()
    if review_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    db.query(Reviews).filter(Reviews.id == review_id).delete()
    db.commit()
