import json
import pytest
from app.database import app
from app.models.model import Event, db
from app.routes.admin_addEvent_routes import event_bp2


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    app.register_blueprint(event_bp2, url_prefix='/api')

    yield client


def test_create_event(client):
    # Test with valid event data
    event_data = {
        "event_title": "Tech Conference 2023",
        "event_type": "Conference",
        "event_description": "A conference on the latest technology trends.",
        "event_date": "2023-12-31",
        "start_time": "09:00:00",
        "end_time": "17:00:00",
        "event_status": "Active"
    }
    response = client.post('/api/events', json=event_data)

    assert response.status_code == 201
    assert 'message' in response.json
    assert response.json['message'] == 'event added successfully'

    # Test with missing required fields
    invalid_event_data = {
        "event_type": "Conference",
        "event_description": "A conference on the latest technology trends.",
        "event_date": "2023-12-31",
        "start_time": "09:00:00",
        "end_time": "17:00:00",
        "event_status": "Active"
    }
    response = client.post('/api/events', json=invalid_event_data)

    assert response.status_code == 400
    assert 'error' in response.json
    assert 'event_title' in response.json['error']

    # Test with invalid event date format
    invalid_date_format_event_data = {
        "event_title": "Tech Conference 2023",
        "event_type": "Conference",
        "event_description": "A conference on the latest technology trends.",
        "event_date": "2023/12/31",  # Invalid date format
        "start_time": "09:00:00",
        "end_time": "17:00:00",
        "event_status": "Active"
    }
    response = client.post('/api/events', json=invalid_date_format_event_data)

    assert response.status_code == 400
    assert 'error' in response.json
    assert 'event_date' in response.json['error']

    # Test with invalid time format
    invalid_time_format_event_data = {
        "event_title": "Tech Conference 2023",
        "event_type": "Conference",
        "event_description": "A conference on the latest technology trends.",
        "event_date": "2023-12-31",
        "start_time": "09:00",  # Invalid time format
        "end_time": "17:00:00",
        "event_status": "Active"
    }
    response = client.post('/api/events', json=invalid_time_format_event_data)

    assert response.status_code == 400
    assert 'error' in response.json
    assert 'start_time' in response.json['error']
