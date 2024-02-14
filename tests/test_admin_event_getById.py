import json
import pytest
from app.database import app
from app.models.model import Event, db
from app.routes.admin_specicEvent_routes import event_bp3


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    app.register_blueprint(event_bp3, url_prefix='/api')

    yield client


def test_get_events_for_user_by_userid(client):
    # Create an event for testing
    event_data = {
        "event_title": "Test Event",
        "event_type": "Test Type",
        "event_description": "This is a test event",
        "event_date": "2023-12-22",
        "start_time": "10:00:00",
        "end_time": "12:00:00",
        "created_at": "2023-12-22 10:00:00",
        "event_status": "Active",
        "updated_at": "2023-12-22 10:30:00",
        "event_location": "Test Location",
        "participants": "Test Participants",
        "devices": "Test Devices"
    }
    response = client.post('/api/single/get_events', json=event_data)

    assert response.status_code == 201

    # Get the event ID from the response
    event_id = json.loads(response.data)['id']

    # Test with a valid event ID
    response = client.get(f'/api/single/get_events/{event_id}')

    assert response.status_code == 200
    assert 'events' in response.json

    event_data = response.json['events'][0]
    assert event_data['Event_Title'] == 'Test Event'
