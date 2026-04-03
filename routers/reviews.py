from typing import Annotated, Optional, ParamSpecArgs
from fastapi import APIRouter, Depends, HTTPException, status, Path
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Reviews
from routers.auth import get_current_user

router = APIRouter(
    prefix='/reviews',
    tags=['reviews']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class ReviewRequest(BaseModel):
    rating: int = Path(gt=0, lt=6)
    comment: str

@router.get('/{listing_id}')
async def read_reviews_on_listing(db:db_dependency, listing_id: int = Path(gt=0)):
    return db.query(Reviews).filter(Reviews.listing_id==listing_id).all()


@router.post('/listing/{listing_id}/reviews', status_code=status.HTTP_201_CREATED)
async def create_review(user: user_dependency, db: db_dependency, review_request: ReviewRequest,
                        listing_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')

    review_model = Reviews(**review_request.model_dump(),listing_id=listing_id, user_id=user.get('id'))
    db.add(review_model)
    db.commit()
    db.refresh(review_model)
    return review_model

@router.put('/{review_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_review(user: user_dependency, db: db_dependency, review_request: ReviewRequest,
                        review_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')

    review_model = db.query(Reviews).filter(Reviews.id==review_id).filter(Reviews.user_id==user.get('id')).first()
    if review_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    review_model.rating = review_request.rating
    review_model.comment = review_request.comment

    db.add(review_model)
    db.commit()

@router.delete('/{review_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(user: user_dependency, db: db_dependency, review_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')

    review_model = db.query(Reviews).filter(Reviews.id==review_id).filter(Reviews.user_id==user.get('id')).first()

    if review_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    db.query(Reviews).filter(Reviews.id == review_id).filter(Reviews.user_id == user.get('id')).delete()
    db.commit()
