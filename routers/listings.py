from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Path
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Listings
from routers.auth import get_current_user

router = APIRouter(
    prefix='/listings',
    tags=['listings']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class ListingRequest(BaseModel):
    title: str
    description: str
    location: str
    address: str
    rooms: int
    floors: int
    property_type: str
    operation_type: str
    price: int

@router.get('/')
async def get_all_user_listings(db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
    return db.query(Listings).filter(Listings.owner_id == user.get('id')).all()

@router.get('/search/')
async def get_searched_listings(db: db_dependency,
        location: Optional[str] = None,
        rooms: Optional[int] = None,
        floors: Optional[int] = None,
        property_type: Optional[str] = None,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None):
    listing_model = db.query(Listings)
    if location:
        listing_model = listing_model.filter(Listings.location.ilike(f"%{location}"))
    if  rooms:
        listing_model = listing_model.filter(Listings.rooms==rooms)
    if floors:
        listing_model = listing_model.filter(Listings.floors==floors)
    if property_type:
        listing_model = listing_model.filter(Listings.property_type==property_type)
    if min_price:
        listing_model = listing_model.filter(Listings.price>=min_price)
    if max_price:
        listing_model = listing_model.filter(Listings.price<=max_price)

    return listing_model.all()


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_new_listing(user: user_dependency, db: db_dependency, listing_request: ListingRequest):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')

    listing_model = Listings(**listing_request.model_dump(), owner_id=user.get('id'))
    db.add(listing_model)
    db.commit()
    db.refresh(listing_model)
    return listing_model

@router.put('/{listing_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_listing(user: user_dependency, db: db_dependency, updated_listing: ListingRequest
                         , listing_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')

    listing_model = (db.query(Listings).filter(Listings.id==listing_id)
                     .filter(Listings.owner_id==user.get('id')).first())

    if listing_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    listing_model.title = updated_listing.title
    listing_model.description = updated_listing.description
    listing_model.location = updated_listing.location
    listing_model.address = updated_listing.address
    listing_model.rooms = updated_listing.rooms
    listing_model.floors = updated_listing.floors
    listing_model.property_type = updated_listing.property_type
    listing_model.operation_type = updated_listing.operation_type
    listing_model.price = updated_listing.price

    db.add(listing_model)
    db.commit()

@router.delete('/{listing_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_listings(user: user_dependency, db: db_dependency, listing_id: int =Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')

    listing_model = (db.query(Listings).filter(Listings.id==listing_id).filter(Listings.owner_id==user.get('id'))
                     .first())
    if listing_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    db.query(Listings).filter(Listings.id == listing_id).filter(Listings.owner_id == user.get('id')).delete()
    db.commit()