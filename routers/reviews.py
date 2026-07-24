import json
from email import message
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session

from database import get_db, redis_client
from models import Reviews, Listings, User
from routers.auth import get_current_user
from schemas import ReviewRequest, ReviewResponse
from services.ws_manager import websocket_manager

router = APIRouter(
    prefix='/reviews',
    tags=['reviews']
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get('/{listing_id}', response_model=List[ReviewResponse])
async def read_reviews_on_listing(db:db_dependency, listing_id: int = Path(gt=0)):
    listing_model = db.query(Listings).filter(Listings.id==listing_id).first()
    if listing_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    return listing_model.reviews

@router.post('/listing/{listing_id}/reviews', status_code=status.HTTP_201_CREATED, response_model=ReviewResponse)
async def create_review(user: user_dependency, db: db_dependency, review_request: ReviewRequest,
                        listing_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')

    review_model = Reviews(**review_request.model_dump(),listing_id=listing_id, user_id=user.get('id'))
    db.add(review_model)
    db.commit()
    db.refresh(review_model)

    listing_model = db.query(Listings).filter(Listings.id==listing_id).first()

    if not listing_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')

    user_model = db.query(User).filter(User.id==user.get('id')).first()

    message = {"type": "new_review", "text": f"{user_model.first_name} написав новий відгук на квартиру!"}
    channel_name = f"notifications:{listing_model.owner_id}"
    await redis_client.publish(channel_name, json.dumps(message))

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
