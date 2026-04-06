import pytest
from .utils import *
from routers.users import get_db, get_current_user
from models import User

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_update_password(test_user):
    request_data = {
        "old_password": "testpassword",
        "new_password": "new_super_password"
    }
    response = client.put('/user/change_password', json=request_data)
    assert response.status_code == 204

def test_update_password_wrong_old_password(test_user):
    request_data = {
        "old_password": "wrongpassword",
        "new_password": "new_super_password"
    }
    response = client.put('/user/change_password', json=request_data)
    assert response.status_code == 401