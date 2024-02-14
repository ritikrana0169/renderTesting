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



def test_delete_event(client):
    # Test case for deleting an existing event
    event_id = 1

    response = client.delete(f'/admin/events/{event_id}')
    assert response.status_code == 200

def test_delete_event_not_found(client):
    # Test case for deleting a non-existing event
    event_id = 999

    response = client.delete(f'/admin/events/{event_id}')
    assert response.status_code == 404
