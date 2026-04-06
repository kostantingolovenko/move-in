from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import pytest

from database import Base
from main import app
from models import User, Listings, Reviews, Favorites, ListingImages
from routers.auth import bcrypt_context

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'email': 'testuser@email.com', 'id': 1, 'role': 'User'}

client = TestClient(app)

@pytest.fixture
def test_user():
    db = TestingSessionLocal()
    db.query(User).delete()
    db.commit()

    user = User(
        email="testuser@email.com",
        first_name="Test",
        last_name="User",
        hashed_password=bcrypt_context.hash("testpassword"),
        role="User",
        phone_number="0991234567"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    yield user

    db.query(User).delete()
    db.commit()
    db.close()


@pytest.fixture
def test_listing(test_user):
    db = TestingSessionLocal()
    db.query(Listings).delete()
    db.commit()

    listing = Listings(
        title="test_listing_title",
        description="Test description for a nice apartment",
        location="Lviv",
        address="Lukasha 5",
        rooms=1,
        floors=5,
        property_type="apartment",
        operation_type="rent",
        price=15000,
        owner_id=test_user.id
    )

    db.add(listing)
    db.commit()
    db.refresh(listing)

    yield listing

    db.query(Listings).delete()
    db.commit()
    db.close()


@pytest.fixture
def test_review(test_listing, test_user):
    db = TestingSessionLocal()
    db.query(Reviews).delete()
    db.commit()

    review = Reviews(
        rating=5,
        comment="Not Bad",
        listing_id=test_listing.id,
        user_id=test_user.id
    )

    db.add(review)
    db.commit()
    db.refresh(review)

    yield review

    db.query(Reviews).delete()
    db.commit()
    db.close()


@pytest.fixture
def test_favorite(test_listing, test_user):
    db = TestingSessionLocal()
    db.query(Favorites).delete()
    db.commit()

    favorite = Favorites(
        listing_id=test_listing.id,
        user_id=test_user.id
    )

    db.add(favorite)
    db.commit()
    db.refresh(favorite)

    yield favorite

    db.query(Favorites).delete()
    db.commit()
    db.close()