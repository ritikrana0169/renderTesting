import pytest
from flask import Flask, json
from app.models.model import db
from app.routes.admin_user_routes import user_blueprint
from app.models.model import User


@pytest.fixture
def app():
    # Create a test Flask app
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    # Initialize SQLAlchemy with the test app
    db.init_app(app)

    # Create the tables in the database
    with app.app_context():
        db.create_all()

    # Register the blueprint
    app.register_blueprint(user_blueprint, url_prefix='/api')

    yield app

    # Drop all tables after the test
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    # Create a test client
    return app.test_client()


def test_register_admin_user_pass(client):
    data = {
        "identifier": "EMP001",
        "role": "User",
        "first_name": "John",
        "last_name": "Doe",
        "address": "123 Main St, City",
        "email": "rm5@gmail.com",
        "phone": "1234567890",
        "password": "Rajeev.1",
        "status": "Active",
        "gender": "Male",
        "created_at": "2023-12-13T12:00:00",
        "updated_at": "2023-12-13T12:30:00"
    }

    # Make a request to the API endpoint
    response = client.post('/api/admin/users', data=json.dumps(data), content_type='application/json')

    # Check if the response is successful (status code 201)
    assert response.status_code == 201

    # Check if the user is registered successfully in the response data
    assert b"User added successfully" in response.data


def test_register_admin_user_fail(client):
    data = {
        "identifier": "EMP001",
        "role": "User",
        "first_name": "John",
        "last_name": "Doe",
        "address": "123 Main St, City",
        "email": "rm56724@gmail.com",
        "phone": "123-456-7890",
        "password": "Rajeev1",
        "status": "Active",
        "created_at": "2023-12-13T12:00:00",
        "updated_at": "2023-12-13T12:30:00"
    }

    # Make a request to the API endpoint
    response = client.post('/api/admin/users', data=json.dumps(data), content_type='application/json')

    # Intentionally create a failing assertion by checking for a condition that is not true
    assert response.status_code == 400  # Change the expected status code to something incorrect

    # Check if the expected error message is in the response data
    expected_error_message = b'{"error":"Invalid password format"}\n'
    assert expected_error_message == response.data


def test_register_admin_user_invalid_role(client):
    data = {
        "role": "InvalidRole",
        "email": "rm56724@gmail.com",
        "password": "Rajeev.1",
        "status": "Active",
        "created_at": "2023-12-13T12:00:00",
        "updated_at": "2023-12-13T12:30:00",
        "images": [
            {
                "url": "https://example.com/image1.jpg",
                "description": "Profile picture"
            }
        ]
    }

    response = client.post('/api/admin/users', data=json.dumps(data), content_type='application/json')

    assert response.status_code == 400
    assert b'{"error":"Invalid role"}' in response.data


def test_register_admin_user_invalid_email_format(client):
    data = {
        "role": "User",
        "email": "rajeev@gmailcom",
        "password": "Rajeev.1",
        "status": "Active",
        "created_at": "2023-12-13T12:00:00",
        "updated_at": "2023-12-13T12:30:00",
        "images": [
            {
                "url": "https://example.com/image1.jpg",
                "description": "Profile picture"
            }
        ]
    }

    response = client.post('/api/admin/users', data=json.dumps(data), content_type='application/json')

    assert response.status_code == 400
    assert b'{"error":"Invalid email format"}' in response.data


def test_register_admin_user_invalid_password_format(client):
    data = {
        "role": "User",
        "email": "rm56724@gmail.com",
        "password": "invalidpassword",
        "status": "Active",
        "created_at": "2023-12-13T12:00:00",
        "updated_at": "2023-12-13T12:30:00",
        "images": [
            {
                "url": "https://example.com/image1.jpg",
                "description": "Profile picture"
            }
        ]
    }

    response = client.post('/api/admin/users', data=json.dumps(data), content_type='application/json')

    assert response.status_code == 400
    assert b'{"error":"Invalid password format"}' in response.data


def test_register_admin_user_invalid_phone_format(client):
    data = {
        "role": "User",
        "email": "rm56724@gmail.com",
        "password": "Rajeev.1",
        "phone": "350958309",
        "status": "Active",
        "created_at": "2023-12-13T12:00:00",
        "updated_at": "2023-12-13T12:30:00",
        "images": [
            {
                "url": "https://example.com/image1.jpg",
                "description": "Profile picture"
            }
        ]
    }

    response = client.post('/api/admin/users', data=json.dumps(data), content_type='application/json')

    assert response.status_code == 400
    assert b'{"error":"Invalid phone number format"}' in response.data


def test_register_admin_user_invalid_status(client):
    data = {
        "role": "User",
        "email": "rm56724@gmail.com",
        "password": "Rajeev.1",
        "phone": "1234567890",
        "status": "InvalidStatus",
        "created_at": "2023-12-13T12:00:00",
        "updated_at": "2023-12-13T12:30:00",
        "images": [
            {
                "url": "https://example.com/image1.jpg",
                "description": "Profile picture"
            }
        ]
    }

    response = client.post('/api/admin/users', data=json.dumps(data), content_type='application/json')

    assert response.status_code == 400
    assert b'{"error":"Invalid status"}' in response.data


# methods to test get all user endpoint
def test_get_all_users_empty_db(client):
    # Make a request to the API endpoint
    response = client.get('/api/admin/users')

    # Check if the response is successful (status code 200)
    assert response.status_code == 200

    # Check if the response contains a message indicating no users in the database
    assert b"No users found in the database" in response.data


def test_get_all_users_with_data(client):
    # Add a test user to the database
    test_user = User(
        identifier="test_user",
        role="admin",
        first_name="Test",
        last_name="User",
        email="test@example.com",
        status="active",
        gender="male"
    )

    with client.application.app_context():
        db.session.add(test_user)
        db.session.commit()

    # Make a request to the API endpoint
    response = client.get('/api/admin/users')

    # Check if the response is successful (status code 200)
    assert response.status_code == 200

    # Check if the response contains data for the added user
    assert b"test_user" in response.data
    assert b"Test" in response.data
    assert b"User" in response.data
    assert b"test@example.com" in response.data


def test_get_all_users_error(client, app):
    # Simulate an error in the service method
    with app.app_context():
        # Assuming you have a mock method for get_all_users that raises an exception
        with pytest.raises(Exception):
            response = client.get('/api/admin/users')

            # Check if the response indicates an internal server error
            assert response.status_code == 500
            assert b"An error occurred" in response.data


# test method for user suggestion endpoint
def test_suggest_usernames(client, app):
    # Add some users to the database for testing suggestions
    user_data = [
        {"first_name": "John", "last_name": "Doe"},
        {"first_name": "Robert", "last_name": "Johnson"},
        {"first_name": "Sophia", "last_name": "Jones"}
    ]

    with app.app_context():
        for data in user_data:
            db.session.add(User(**data))
        db.session.commit()

    # Make a request to the API endpoint to suggest usernames for "Jon"
    response = client.get('/api/admin/users/suggest?name=john')

    # Check if the response is successful (status code 200)
    assert response.status_code == 200

    # Check if the expected suggestions are present in the response data
    expected_suggestions = [
        {"full_name": "John Doe", "id": 1},
        {"full_name": "Robert Johnson", "id": 2}
    ]

    response_data = json.loads(response.data)
    assert response_data["suggested_users"] == expected_suggestions
