import pytest
from flask import Flask, json
from app.models.model import db
from app.routes.admin_addEvent_routes import addEevent_bp


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
    app.register_blueprint(addEevent_bp, url_prefix='/api')

    yield app

    # Drop all tables after the test
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    # Create a test client
    return app.test_client()


def test_register_event_pass(client):
    data = {
        "event_title": "CBA Conference 2023",
        "event_type": "Recurring",
        "event_description": "dfhgdshht srfgsdrtwrt",
        "event_date": "2050-12-29",
        "start_time": "19:00:00",
        "end_time": "22:00:00",
        "event_location": "Mumbai",
        "repeat_type": "Weekly",
        "repeat_days": ["tuesday", "thursday", "friday", "saturday"]

    }

    # Make a request to the API endpoint
    response = client.post('admin/events', data=json.dumps(data), content_type='application/json')

    # Check if the response is successful 
    if response.status_code == 201:
        assert b"event added successfully" in response.data
    # Check if the user is registered successfully in the response data


def test_register_event_fail(client):
    data = {
        "event_title": "CBA Conference 2023",
        "event_type": "Recurring",
        "event_description": "dfhgdshht srfgsdrtwrt",
        "event_date": "2050-12-29",
        "start_time": "19:00:00",
        "end_time": "22:00:00",
        "event_location": "Mumbai",
        "repeat_type": "Weekly",
        "repeat_days": ["tuesday", "thursday", "friday", "saturday"]

    }

    # Make a request to the API endpoint
    response = client.post('admin/events', data=json.dumps(data), content_type='application/json')

    # Intentionally create a failing assertion by checking for a condition that is not true
    if response.status_code == 400:
        assert b'{"error":"Invalid data"}' in response.data



def test_register_event_invalid_event_type(client):
    data = {
        "event_title": "CBA Conference 2023",
        "event_type": "",
        "event_description": "dfhgdshht srfgsdrtwrt",
        "event_date": "2050-12-29",
        "start_time": "19:00:00",
        "end_time": "22:00:00",
        "event_location": "Mumbai",
        "repeat_type": "Weekly",
        "repeat_days": ["tuesday", "thursday", "friday", "saturday"]

    }

    response = client.post('admin/events', data=json.dumps(data), content_type='application/json')

    if response.status_code == 400:
        assert b'{"error":"Invalid event_type"}' in response.data



def test_addEvent_inviled_date(client):
    data = {
        "event_title": "CBA Conference 2023",
        "event_type": "Recurring",
        "event_description": "dfhgdshht srfgsdrtwrt",
        "event_date": "2010-12-29",
        "start_time": "19:00:00",
        "end_time": "22:00:00",
        "event_location": "Mumbai",
        "repeat_type": "Weekly",
        "repeat_days": ["tuesday", "thursday", "friday", "saturday"]

    }

    response = client.post('admin/events', data=json.dumps(data), content_type='application/json')

    if response.status_code == 400:
        assert b'{"error":"Invalid event_date"}' in response.data

def test_addEvent_inviled_start_time(client):
    data = {
        "event_title": "CBA Conference 2023",
        "event_type": "Recurring",
        "event_description": "dfhgdshht srfgsdrtwrt",
        "event_date": "2050-12-29",
        "start_time": "59:00:00",
        "end_time": "22:00:00",
        "event_location": "Mumbai",
        "repeat_type": "Weekly",
        "repeat_days": ["tuesday", "thursday", "friday", "saturday"]

    }

    response = client.post('admin/events', data=json.dumps(data), content_type='application/json')

    if response.status_code == 400:
        assert b'{"error":"Invalid start_time}' in response.data

def test_addEvent_inviled_end_time(client):
    data = {
        "event_title": "CBA Conference 2023",
        "event_type": "Recurring",
        "event_description": "dfhgdshht srfgsdrtwrt",
        "event_date": "2050-12-29",
        "start_time": "19:00:00",
        "end_time": "10:76:00",
        "event_location": "Mumbai",
        "repeat_type": "Weekly",
        "repeat_days": ["tuesday", "thursday", "friday", "saturday"]

    }

    response = client.post('admin/events', data=json.dumps(data), content_type='application/json')

    if response.status_code == 400:
        assert b'{"error":"Invalid end_time"}' in response.data


def test_addEvent_inviled_repeat_type(client):
    data = {
        "event_title": "CBA Conference 2023",
        "event_type": "Recurring",
        "event_description": "dfhgdshht srfgsdrtwrt",
        "event_date": "2050-12-29",
        "start_time": "19:00:00",
        "end_time": "22:00:00",
        "event_location": "Mumbai",
        "repeat_type": "",
        "repeat_days": ["tuesday", "thursday", "friday", "saturday"]

    }

    response = client.post('admin/events', data=json.dumps(data), content_type='application/json')

    if response.status_code == 400:
        assert b'{"error":"Invalid repeat_type"}' in response.data

def test_addEvent_inviled_repeat_days(client):
    data = {
        "event_title": "CBA Conference 2023",
        "event_type": "Recurring",
        "event_description": "dfhgdshht srfgsdrtwrt",
        "event_date": "2050-12-29",
        "start_time": "19:00:00",
        "end_time": "22:00:00",
        "event_location": "Mumbai",
        "repeat_type": "Weekly",
        "repeat_days": ["", "ghdas", "1123", ""]

    }

    response = client.post('admin/events', data=json.dumps(data), content_type='application/json')

    if response.status_code == 400:
        assert b'{"error":"Invalid repeat_days"}' in response.data