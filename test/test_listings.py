import pytest
from .utils import *
from routers.listings import get_db, get_current_user
from models import Listings

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_all_user_listings(test_listing):
    response = client.get("/listings/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]['title'] == 'test_listing_title'


def test_search_listings_with_pagination(test_listing):
    response = client.get("/listings/search/?location=Київ&limit=10&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert type(data) == list


def test_create_listing(test_user):
    request_data = {
        'title': 'Крута квартира в центрі',
        'description': 'Супер ремонт, панорамні вікна',
        'location': 'Київ',
        'address': 'Хрещатик 1',
        'rooms': 2,
        'floors': 5,
        'property_type': 'apartment',
        'operation_type': 'rent',
        'price': 20000
    }

    response = client.post('/listings/', json=request_data)
    assert response.status_code == 201

    db = TestingSessionLocal()
    model = db.query(Listings).filter(Listings.title == 'Крута квартира в центрі').first()
    assert model is not None
    assert model.price == 20000
    assert model.owner_id == test_user.id


def test_delete_listing(test_listing):
    response = client.delete(f'/listings/{test_listing.id}')
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Listings).filter(Listings.id == test_listing.id).first()
    assert model is None


def test_upload_listing_image(test_listing):
    file_content = b"fake image bytes"
    files = {'file': ('test_image.jpg', file_content, 'image/jpeg')}

    response = client.post(f'/listings/{test_listing.id}/images/', files=files)

    assert response.status_code == 201
    data = response.json()
    assert data['message'] == "Image uploaded successfully"
    assert "static/images/" in data['image_url']