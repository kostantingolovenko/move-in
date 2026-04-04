from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Annotated

from models import Favorites, Listings
from routers.auth import get_current_user

router = APIRouter(
    prefix='/favorites',
    tags=['favorites']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get('/')
async def read_user_favorites(user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')

    return db.query(Favorites).filter(Favorites.user_id==user.get('id')).all()

@router.post('/{listing_id}', status_code=status.HTTP_201_CREATED)
async def create_favorite(user: user_dependency, db: db_dependency, listing_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')

    listing_model = db.query(Listings).filter(Listings.id==listing_id).first()
    if listing_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    favorite_model = Favorites(user_id=user.get('id'), listing_id=listing_id)
    db.add(favorite_model)
    db.commit()
    db.refresh(favorite_model)
    return favorite_model

@router.delete('/{listing_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_favorite(user: user_dependency, db: db_dependency, listing_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')

    favorite_model = (db.query(Favorites).filter(Favorites.id==listing_id)
                      .filter(Favorites.user_id==user.get('id')).first())

    if favorite_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    db.query(Favorites).filter(Favorites.id == listing_id).filter(Favorites.user_id == user.get('id')).delete()
    db.commit()