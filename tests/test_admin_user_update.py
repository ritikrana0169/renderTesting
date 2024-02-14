import json
import pytest

from app.database import app
from app.models.model import User, db
from app.routes.admin_user_update_route import update_users_blueprint
from app.routes.admin_user_routes import user_blueprint


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    # Set up the database if not exist
    with app.app_context():
        db.create_all()

    app.register_blueprint(update_users_blueprint, url_prefix='/api')
    app.register_blueprint(user_blueprint, url_prefix='/api')

    yield client


def test_update_user(client):
    # Create a user for testing
    user_data = {
        "identifier": "test123",
        "role": "User",
        "first_name": "Raj",
        "last_name": "Kumar",
        "email": "raj@gmail.com",
        "password": "Test@123",
        "address": "Delhi",
        "phone": "1234567890",
        "status": "Active"
    }
    response = client.post('/api/admin/users', json=user_data)

    assert response.status_code == 201

    # Get the user ID from the response
    user_id = json.loads(response.data)['id']

    # Update user data
    update_data = {
        "role": "Admin",
        "first_name": "UpdatedFirstName",
        "email": "updated_email@gmail.com",
        "password": "UpdatedPassword@123",
        "status": "Inactive"
    }

    # Send the update request
    response = client.put(f'/api/admin/users/{user_id}', json=update_data)
    assert response.status_code == 200
    assert json.loads(response.data)['message'] == 'User details updated successfully'

    # Test invalid role
    invalid_role_data = {'role': 'InvalidRole'}
    response = client.put(f'/api/admin/users/{user_id}', json=invalid_role_data)
    assert response.status_code == 400
    assert json.loads(response.data)['error'] == 'Invalid role'

    # Test invalid email format
    invalid_email_data = {'email': 'invalid-email'}
    response = client.put(f'/api/admin/users/{user_id}', json=invalid_email_data)
    assert response.status_code == 400
    assert json.loads(response.data)['error'] == 'Invalid email format'

    # Test invalid password format
    invalid_password_data = {'password': 'short'}
    response = client.put(f'/api/admin/users/{user_id}', json=invalid_password_data)
    assert response.status_code == 400
    assert json.loads(response.data)['error'] == 'Invalid password format'

    # Test invalid status
    invalid_status_data = {'status': 'InvalidStatus'}
    response = client.put(f'/api/admin/users/{user_id}', json=invalid_status_data)
    assert response.status_code == 400
    assert json.loads(response.data)['error'] == 'Invalid status'

    # Test updating non-existent user
    response = client.put('/api/admin/users/999', json=update_data)
    assert response.status_code == 404
    assert json.loads(response.data)['error'] == 'User not found'

