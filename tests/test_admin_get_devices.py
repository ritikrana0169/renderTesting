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





def test_get_all_devices(client, app):
    # Add test devices to the database
    test_devices = [
        {"name": "Device1", "ip_address": "192.168.1.1", "location": "Location1"},
        {"name": "Device2", "ip_address": "192.168.1.2", "location": "Location2"}
    ]

    with app.app_context():
        for device_data in test_devices:
            device = Device(**device_data)
            db.session.add(device)
        db.session.commit()

    # Make a request to the API endpoint to get all devices
    response = client.get('/api/admin/devices')

    # Check if the response is successful (status code 200)
    assert response.status_code == 200

    # Check if the response contains data for the added devices
    assert b"Device1" in response.data
    assert b"Device2" in response.data
    # Add more assertions based on your actual data structure and response format
