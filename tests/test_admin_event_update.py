import json
import pytest
from flask import Flask

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_update_event(client):
    # Test case for updating an existing event
    event_id = 1
    data = {
        'start_time': '2023-01-01 10:00:00',
        'end_time': '2023-01-01 12:00:00',
        'event_title': 'Updated Event',
        'event_type': 'Meeting',
        'event_description': 'Updated description',
        'status': 'updated'
    }

    response = client.put(f'/admin/events/{event_id}', json=data)
    assert response.status_code == 200

def test_update_event_invalid_date_format(client):
    # Test case for updating an event with invalid date format
    event_id = 1
    data = {
        'start_time': '2023-01-01 10:00:00',
        'end_time': 'invalid_date_format',
    }

    response = client.put(f'/admin/events/{event_id}', json=data)
    assert response.status_code == 400

