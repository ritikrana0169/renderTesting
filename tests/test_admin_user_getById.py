import json

import pytest

from app.database import app
from app.models.model import User, db
# from app.routes.admin_user_get_route import get_user_blueprint
from app.routes.admin_user_routes import user_blueprint


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    app.register_blueprint(user_blueprint, url_prefix='/api')

    yield client


def test_update_user(client):
    # Create a user for testing
    user_data = {
        "identifier": "test123",
        "role": "User",
        "first_name": "Johnny",
        "last_name": "Doe",
        "email": "johnDoe@gmail.com",
        "password": "Testy@123",
        "address": "123 Main St",
        "phone": "1234567890",
        "status": "Active"
    }
    response = client.post('/api/admin/users', json=user_data)

    assert response.status_code == 201

    # Get the user ID from the response
    user_id = json.loads(response.data)['id']
    
    response = client.get(f'/api/admin/users/{user_id}')

    assert response.status_code == 200
    assert 'user' in response.json
    
    user_data = response.json['user']
    assert user_data['id'] == user_id
    assert user_data['role'] == 'User'
    assert user_data['first_name'] == 'Johnny'
    assert user_data['last_name'] == 'Doe'
    assert user_data['email'] == 'johnDoe@gmail.com'
    assert user_data['status'] == 'Active'

    # Test with an invalid user ID
    response = client.get('/api/admin/users/0')

    assert response.status_code == 400
    assert 'error' in response.json
    assert response.json['error'] == 'Invalid user ID'

    # Test with a user ID that doesn't exist in the database
    response = client.get('/api/admin/users/999')

    assert response.status_code == 404
    assert 'error' in response.json
    assert response.json['error'] == 'User not found'
