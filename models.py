from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

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

    listings = relationship("Listings", back_populates='owner', cascade="all, delete-orphan")
    reviews = relationship("Reviews", back_populates='user', cascade="all, delete-orphan")
    favorites = relationship("Favorites", back_populates='user', cascade="all, delete-orphan")

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

    owner = relationship("User", back_populates='listings')
    reviews = relationship("Reviews", back_populates='listing', cascade="all, delete-orphan")
    favorited_by = relationship("Favorites", back_populates='listing', cascade="all, delete-orphan")
    images = relationship("ListingImages", back_populates='listing', cascade="all, delete-orphan")

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

    user = relationship("User", back_populates='reviews')
    listing = relationship('Listings', back_populates='reviews')

class Favorites(Base):
    __tablename__ = 'favorites'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    listing_id = Column(Integer, ForeignKey('listings.id'))
    added_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates='favorites')
    listing = relationship("Listings", back_populates='favorited_by')

class ListingImages(Base):
    __tablename__ = 'listing_images'

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String)
    listing_id = Column(Integer, ForeignKey('listings.id'))

    listing = relationship('Listings', back_populates='images')