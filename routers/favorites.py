from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from typing import Annotated

from models import Favorites, Listings, User
from routers.auth import get_current_user
from database import get_db

router = APIRouter(
    prefix='/favorites',
    tags=['favorites']
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get('/')
async def read_user_favorites(user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')

    user_model = db.query(User).filter(User.id==user.get('id')).first()
    return user_model.favorites

@router.post('/{listing_id}', status_code=status.HTTP_201_CREATED)
async def create_favorite(user: user_dependency, db: db_dependency, listing_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')

    listing_model = db.query(Listings).filter(Listings.id==listing_id).first()
    if listing_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    already_favorite = (db.query(Favorites).filter(Favorites.listing_id==listing_id, Favorites.user_id ==user.get('id'))
                        .first())
    if already_favorite:
        return {"message": "Already in favorites", "success": True}

    favorite_model = Favorites(user_id=user.get('id'), listing_id=listing_id)

    db.add(favorite_model)
    db.commit()
    db.refresh(favorite_model)
    return favorite_model

@router.delete('/{favorite_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_favorite(user: user_dependency, db: db_dependency, favorite_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')

    favorite_model = (db.query(Favorites).filter(Favorites.id==favorite_id)
                      .filter(Favorites.user_id==user.get('id')).first())

    if favorite_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    db.query(Favorites).filter(Favorites.id == favorite_id).filter(Favorites.user_id == user.get('id')).delete()
    db.commit()