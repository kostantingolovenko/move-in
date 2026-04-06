import pytest
from jose import jwt
from datetime import timedelta
from fastapi import HTTPException

from .utils import *
from routers.auth import get_db, get_current_user, authenticate_user, create_access_token, SECRET_KEY, ALGORITHM
from models import User

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_create_user():
    request_body = {
        'first_name': 'Ivan',
        'last_name': 'Franko',
        'email': 'new_unique_email@gmail.com',
        'phone_number': '0990001122',
        'password': 'strongpassword123',
        'role': 'User'
    }

    response = client.post('/auth', json=request_body)
    assert response.status_code == 201

    db = TestingSessionLocal()
    model = db.query(User).filter(User.email == 'new_unique_email@gmail.com').first()
    assert model is not None
    assert model.phone_number == '0990001122'

def test_authenticate_user(test_user):
    db = TestingSessionLocal()
    authenticated_user = authenticate_user(test_user.email, 'testpassword', db)
    assert authenticated_user is not None
    assert authenticated_user.email == test_user.email

    non_existent_user = authenticate_user('wrong@email.com', '12345', db)
    assert non_existent_user is False