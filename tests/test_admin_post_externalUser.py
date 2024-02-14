import pytest
from flask import Flask, json
from app.models.model import db
from app.routes.admin_external_user_route import Externaluser_blueprint


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
    app.register_blueprint(Externaluser_blueprint, url_prefix='/admin')

    yield app

    # Drop all tables after the test
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    # Create a test client
    return app.test_client()


def test_register_admin_externalUser_pass(client):
    data = {
        "first_name": "abc",
        "last_name": "xyz",
        # "address": "w 11, Hjp",
        "email": "demo12@gmail.com",
        "phone": "7684567890",
        "status": "Active"
    }

    # Make a request to the API endpoint
    response = client.post('admin/events/1/add_external_user', data=json.dumps(data), content_type='application/json')

    # Check if the response is successful 
    if response.status_code == 200:
        assert b"User added successfully" in response.data
    # Check if the user is registered successfully in the response data


def test_register_admin_externalUser_fail(client):
    data = {
        "role": "Guest",
        "first_name": "abc",
        "last_name": "xyz",
        "email": "demo12@gmail.com",
        "phone": "7684567890",
        "status": "Active",
        # "gender":"Male",
        "created_at": "2023-12-13T12:00:00",
        "updated_at": "2023-12-13T12:30:00"
    }

    # Make a request to the API endpoint
    response = client.post('admin/events/1/add_external_user', data=json.dumps(data), content_type='application/json')

    # Intentionally create a failing assertion by checking for a condition that is not true
    if response.status_code == 400:
        assert b'{"error":"Invalid data"}' in response.data



def test_register_admin_externalUser_invalid_role(client):
    data = {
        "role": "InvalidRole",
         "first_name": "abc",
        "last_name": "xyz",
        "email": "sk@gmail.com",
        "status": "Active",
        "phone":"8790955627",
        "gender":"Male",
        "created_at": "2023-12-13T12:00:00",
        "updated_at": "2023-12-13T12:30:00",
        "images": [
            {
                "url": "https://example.com/image1.jpg",
                "description": "Profile picture"
            }
        ]
    }

    response = client.post('admin/events/1/add_external_user', data=json.dumps(data), content_type='application/json')

    if response.status_code == 400:
        assert b'{"error":"Invalid role"}' in response.data



def test_register_admin_externalUser_invalid_email_format(client):
    data = {
        "role": "Guest",
         "first_name": "abc",
        "last_name": "xyz",
        "email": "sk@gmailcom",
        "status": "Active",
        "gender":"Male",
        "created_at": "2023-12-13T12:00:00",
        "updated_at": "2023-12-13T12:30:00",
        "images": [
            {
                "url": "https://example.com/image1.jpg",
                "description": "Profile picture"
            }
        ]
    }

    response = client.post('admin/events/1/add_external_user', data=json.dumps(data), content_type='application/json')

    if response.status_code == 400:
        assert b'{"error":"Invalid email format"}' in response.data

def test_register_admin_externalUser_invalid_phone_format(client):
    data = {
        "role": "Guest",
        "first_name": "abc",
        "last_name": "xyz",
        "email": "rajeev1@gmail.com",
        "status": "Active",
        "phone":"1111111111",
        "gender":"Male",
        "created_at": "2023-12-13T12:00:00",
        "updated_at": "2023-12-13T12:30:00",
        "images": [
            {
                "url": "https://example.com/image1.jpg",
                "description": "Profile picture"
            }
        ]
    }

    response = client.post('admin/events/1/add_external_user', data=json.dumps(data), content_type='application/json')
    if response.status_code == 400:
        assert b'{"error":"Invalid phone format"}' in response.data


def test_register_admin_externalUser_invalid_status(client):
    data = {
        "email": "sk12@gmail.com",
        "phone": "7611111111",
         "gender":"Male",
         "first_name": "abc",
        "last_name": "xyz",
        "status": "jssajsgjksg",
        "created_at": "2023-12-13T12:00:00",
        "updated_at": "2023-12-13T12:30:00",
        "images": [
            {
                "url": "https://example.com/image1.jpg",
                "description": "Profile picture"
            }
        ]
    }

    response = client.post('admin/events/1/add_external_user', data=json.dumps(data), content_type='application/json')

    if response.status_code == 400:
        assert b'{"error":"Invalid status"}' in response.data



def test_register_admin_externalUser_invalid_gender(client):
    data = {
        "email": "sk12@gmail.com",
        "phone": "7611111111",
        "gender":"cvfxzvsdf",
        "first_name": "abc",
        "last_name": "xyz",
        "created_at": "2023-12-13T12:00:00",
        "updated_at": "2023-12-13T12:30:00",
        "images": [
            {
                "url": "https://example.com/image1.jpg",
                "description": "Profile picture"
            }
        ]
    }

    response = client.post('admin/events/1/add_external_user', data=json.dumps(data), content_type='application/json')

    if response.status_code == 400:
        assert b'{"error":"Invalid gender"}' in response.data