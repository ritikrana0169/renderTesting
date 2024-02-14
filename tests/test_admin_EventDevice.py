import pytest
from flask import Flask
from app.models.model import db, Event, Device
from app.services.admin_device_service import admin_eventdevice_servic
from app.routes.admin_device_routes import eventDevice_routes


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
    app.register_blueprint(eventDevice_routes, url_prefix='/eventDevice')

    yield app

    # Drop all tables after the test
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    # Create a test client
    return app.test_client()


def test_add_device_to_event(client):
    # Create a test event and device
    with client.application.app_context():
        event = Event(event_title='Test Event', event_type='Test Type')
        device = Device(name='Test Device', ip_address='127.0.0.1', location='Test Location')

        # Add the event and device to the database
        db.session.add(event)
        db.session.add(device)
        db.session.commit()

        # Make a request to the API endpoint
        response = client.post('/eventDevice/admin/events/{}/add_device/{}'.format(event.id, device.id))

        # Check if the response is successful (status code 200)
        assert response.status_code == 200

        # Check if the device is added to the event in the database
        updated_event = db.session.query(Event).get(event.id)

        assert device in updated_event.devices


def test_get_devices_for_event(client):
    # Create a test event and devices
    with client.application.app_context():
        event = Event(event_title='Test Event', event_type='Test Type')
        device1 = Device(name='Device 1', ip_address='127.0.0.1', location='Location 1')
        device2 = Device(name='Device 2', ip_address='127.0.0.2', location='Location 2')

        # Add the event and devices to the database
        db.session.add(event)
        db.session.add(device1)
        db.session.add(device2)
        event.devices.extend([device1, device2])
        db.session.commit()

        # Make a request to the API endpoint
        response = client.get('/eventDevice/admin/events/{}/devices'.format(event.id))

        # Check if the response is successful (status code 200)
        assert response.status_code == 200

        # Check if the response data contains information about the devices
        devices_data = response.get_json()
        assert len(devices_data) == 2
        # You can add more specific assertions based on your expected response format

def test_remove_device_from_event(client):
    
    # Create a test event and device
    with client.application.app_context():
        event = Event(event_title='Test Event', event_type='Test Type')
        device = Device(name='Test Device', ip_address='127.0.0.1', location='Test Location')

        # Add the event and device to the database
        db.session.add(event)
        db.session.add(device)
        event.devices.append(device)
        db.session.commit()

        # Make a request to the API endpoint
        response = client.delete('/eventDevice/admin/events/{}/add_device/{}'.format(event.id, device.id))

        # Check if the response is successful (status code 200)
        assert response.status_code == 200

        # Check if the device is removed from the event in the database
        updated_event = Event.query.get(event.id)
        assert device not in updated_event.devices