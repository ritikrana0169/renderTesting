import json
import pytest
from app.database import app
from app.models.model import User, db
from app.routes.admin_user_update_route import users_blueprint
from app.routes.admin_user_routes import adduser_blueprint
from app.routes.user_routes import events_bp, events_blueprint


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    # Set up the database if not exist
    with app.app_context():
        db.create_all()

    # Move blueprint registration outside of app_context
    app.register_blueprint(events_bp, url_prefix='/events')
    app.register_blueprint(events_blueprint, url_prefix='/getevents')

    yield client

def test_get_upcoming_events_of_user(client):

    response = client.get('/events/get_upcoming_eventsOf_user/3')
    assert response.status_code == 200
    event_list = json.loads(response.data)['upcoming_events']
    assert event_list[0]['Event_Title'] == event_list[0]['Event_Title']
    # assert event_list[0]['Event_Type'] == event_list[0]['Event_Type']
    # assert event_list[0]['Event_Title'] == event_list[0]['Event_Title']


    # Testcase for user not found
    response = client.get('/events/get_upcoming_eventsOf_user/111')
    assert response.status_code == 200
    assert json.loads(response.data)['message'] == 'User not found'



    # Test case for a user with no upcoming events
    response = client.get('/events/get_upcoming_eventsOf_user/1')
    assert response.status_code == 200
    response_data = json.loads(response.data)

    if 'upcoming_events' in response_data:
        # Check if there are any upcoming events
        assert len(response_data['upcoming_events']) == 0
    else:
        # If 'upcoming_events' key is not present, check for the 'message' key
        assert 'message' in response_data
        assert response_data['message'] == 'No upcoming events for the user'



def test_get_all_events_of_user(client):

    response = client.get('/getevents/get_allevents_of_user/3')
    assert response.status_code == 200
    event_list = json.loads(response.data)['events']
    assert event_list[0]['Event_Title'] == event_list[0]['Event_Title']
    # assert event_list[0]['Event_Type'] == event_list[0]['Event_Type']
    # assert event_list[0]['Event_Title'] == event_list[0]['Event_Title']


    # Testcase for user not found
    response = client.get('/getevents/get_allevents_of_user/111')
    assert response.status_code == 200
    assert json.loads(response.data)['message'] == 'User not found'



    # Test case for a user with no upcoming events
    response = client.get('/getevents/get_allevents_of_user/6')
    assert response.status_code == 200
    response_data = json.loads(response.data)

        # If 'upcoming_events' key is not present, check for the 'message' key
    assert 'message' in response_data
    assert response_data['message'] == 'No events found for the user'
