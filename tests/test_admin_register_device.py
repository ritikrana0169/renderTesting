# test_admin_register_device.py
import json
import pytest
from flask import Flask, json
from app.models.model import db, Device
from app.routes.admin_register_device_routes import device_routes


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
    app.register_blueprint(device_routes, url_prefix='/api')

    yield app

    # Drop all tables after the test
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    # Create a test client
    return app.test_client()


def test_add_new_device_success(client):
    data = {
        "name": "TestDevice",
        "ip_address": "192.168.1.1",
        "location": "TestLocation"
    }

    # Make a request to the API endpoint
    response = client.post('/api/admin/device', data=json.dumps(data), content_type='application/json')

    # Check if the response is successful (status code 201)
    assert response.status_code == 201

    # Check if the device is added successfully in the response data
    assert b"Device added successfully" in response.data

    # Check if the device id is present in the response data
    assert b"id" in response.data


# from app.database import app

def test_add_new_device_duplicate(client, app):

    # Add a device with the same name, ip_address, and location
    existing_device = Device(
        name="TestDevice",
        ip_address="192.168.1.1",
        location="TestLocation"
    )

    # Use the app context to interact with the database
    with app.app_context():
        db.create_all()  # Make sure to create the necessary tables
        db.session.add(existing_device)
        db.session.commit()

    data = {
        "name": "TestDevice",
        "ip_address": "192.168.1.1",
        "location": "TestLocation"
    }

    # Make a request to the API endpoint
    response = client.post('/api/admin/device', data=json.dumps(data), content_type='application/json')

    # Check if the response has an error due to duplicate device
    assert response.status_code == 400
    assert b"Device with the same name, IP address, and location already exists" in response.data


def test_add_new_device_invalid_ip_address(client):
    data = {
        "name": "TestDevice",
        "ip_address": "invalid_ip",  # Invalid IP address format
        "location": "TestLocation"
    }

    # Make a request to the API endpoint
    response = client.post('/api/admin/device', data=json.dumps(data), content_type='application/json')

    # Check if the response has a JSON error message due to an invalid IP address
    assert response.status_code == 400
    assert b"Invalid IP address format" in response.data
