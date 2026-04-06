import pytest
from .utils import *
from routers.reviews import get_db, get_current_user
from models import Reviews

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_get_listing_reviews(test_listing, test_review):
    response = client.get(f'/reviews/{test_listing.id}')

    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]['rating'] == 5
    assert data[0]['comment'] == "Not Bad"


def test_create_review(test_listing):
    request_data = {
        "rating": 4,
        "comment": "All good."
    }

    response = client.post(f'/reviews/listing/{test_listing.id}/reviews', json=request_data)
    assert response.status_code == 201

    db = TestingSessionLocal()
    model = db.query(Reviews).filter(Reviews.listing_id == test_listing.id).first()
    assert model is not None
    assert model.rating == 4
    assert model.comment == request_data["comment"]
    assert model.user_id == 1


def test_create_review_invalid_rating(test_listing):
    request_data = {
        "rating": 10,
        "comment": "Нереально круто"
    }

    response = client.post(f'/reviews/listing/{test_listing.id}/reviews', json=request_data)
    assert response.status_code == 422


def test_delete_review(test_review):
    response = client.delete(f'/reviews/{test_review.id}')

    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Reviews).filter(Reviews.id == test_review.id).first()
    assert model is None