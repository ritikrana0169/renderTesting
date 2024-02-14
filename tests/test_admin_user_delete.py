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
    app.register_blueprint(user_blueprint, url_prefix='/api', name='user')

    yield client


def test_delete_user(client):
    # Create a user for testing
    user_data = {
            "identifier": "asd123",
            "role": "User",
            "first_name": "Ankit",
            "last_name": "Kumar",
            "email": "ankit@gmail.com",
            "password": "Ankit@123",
            "address": "Delhi",
            "phone": "1234567890",
            "status": "Active",
            "gender": "Male"
        }
    response = client.post('/api/admin/users', json=user_data)

    assert response.status_code == 201

    # Get the user ID from the response
    user_id = json.loads(response.data)['id']

    # Make a DELETE request to delete the user
    response = client.delete(f'api/admin/users/{user_id}')

    assert response.status_code == 200
    assert 'User deleted successfully' in response.get_data(as_text=True)

    # Make a DELETE request with a user_id that does not exist
    response = client.delete('api/admin/users/999')

    assert response.status_code == 404
    assert 'User not found' in response.get_data(as_text=True)
