from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    phone_number = Column(String, unique=True)
    hashed_password = Column(String)
    role = Column(String, default='User')
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda : datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda : datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))

class Listings(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    location = Column(String)
    address = Column(String)
    rooms = Column(Integer)
    floors = Column(Integer)
    property_type = Column(String)
    operation_type = Column(String)
    price = Column(Integer)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))
    owner_id = Column(Integer, ForeignKey('users.id'))

class Reviews(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer)
    comment= Column(String)
    listing_id = Column(Integer, ForeignKey('listings.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))

class Favorites(Base):
    __tablename__ = 'favorites'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    listing_id = Column(Integer, ForeignKey('listings.id'))
    added_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))