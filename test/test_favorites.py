import pytest
from .utils import *
from routers.favorites import get_db, get_current_user
from models import Favorites

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_get_user_favorites(test_listing, test_favorite):
    response = client.get('/favorites/')

    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]['listing_id'] == test_listing.id


def test_add_to_favorites(test_listing):
    response = client.post(f'/favorites/{test_listing.id}')

    assert response.status_code == 201

    db = TestingSessionLocal()
    model = db.query(Favorites).filter(Favorites.listing_id == test_listing.id).first()
    assert model is not None
    assert model.user_id == 1


def test_add_to_favorites_not_found():
    response = client.post('/favorites/9999')
    assert response.status_code == 404


def test_delete_from_favorites(test_listing, test_favorite):
    response = client.delete(f'/favorites/{test_favorite.id}')
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Favorites).filter(Favorites.id == test_favorite.id).first()
    assert model is None