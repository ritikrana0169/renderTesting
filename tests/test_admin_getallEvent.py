import pytest
from flask import Flask, json
from app.models.model import db
from app.models.model import all_event_bp  
from app.routes.admin_event_routes import all_event_bp

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
    app.register_blueprint(all_event_bp, url_prefix='/allevents')  # Adjust the URL prefix accordingly

    yield app

    # Drop all tables after the test
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    # Create a test client
    return app.test_client()

def test_get_all_events_for_user(client, mocker):
    # Mock the EventService to return a list of mock events
    mocker.patch.object(EventService, 'get_events_for_user', return_value=[
        MockEvent(
            event_title='Mock Event 1',
            event_type='Mock Type 1',
            event_description='Mock Description 1',
            event_date='2023-12-25',
            start_time=datetime(2023, 12, 25, 10, 0, 0),
            end_time=datetime(2023, 12, 25, 12, 0, 0),
            created_at=datetime(2023, 12, 25, 8, 0, 0),
            event_status='Mock Status 1',
            updated_at=datetime(2023, 12, 25, 9, 0, 0),
            event_location='Mock Location 1',
            participants=['Participant 1', 'Participant 2'],
            devices=['Device 1', 'Device 2']
        ),
        MockEvent(
            event_title='Mock Event 2',
            event_type='Mock Type 2',
            event_description='Mock Description 2',
            event_date='2023-12-26',
            start_time=datetime(2023, 12, 26, 14, 0, 0),
            end_time=datetime(2023, 12, 26, 16, 0, 0),
            created_at=datetime(2023, 12, 26, 12, 0, 0),
            event_status='Mock Status 2',
            updated_at=datetime(2023, 12, 26, 13, 0, 0),
            event_location='Mock Location 2',
            participants=['Participant 3', 'Participant 4'],
            devices=['Device 3', 'Device 4']
        )
    ])

   # Make a request to the API endpoint
    response = client.get('/allevents/get_allevents')

    # Check if the response is successful (status code 200)
    assert response.status_code == 200

    # Check if the expected events are present in the response data
    expected_events = [
        {
            'Event_Title': 'Mock Event 1',
            'Event_Type': 'Mock Type 1',
            'Event_Description': 'Mock Description 1',
            'Event_Date': '2023-12-25',
            'Start_Time': '10:00:00',
            'End_Time': '12:00:00',
            'created_at': '2023-12-25T08:00:00',
            'event_status': 'Mock Status 1',
            'updated_at': '2023-12-25T09:00:00',
            'event_location': 'Mock Location 1',
            'participants': ['Participant 1', 'Participant 2'],
            'devices': ['Device 1', 'Device 2']
        },
        {
            'Event_Title': 'Mock Event 2',
            'Event_Type': 'Mock Type 2',
            'Event_Description': 'Mock Description 2',
            'Event_Date': '2023-12-26',
            'Start_Time': '14:00:00',
            'End_Time': '16:00:00',
            'created_at': '2023-12-26T12:00:00',
            'event_status': 'Mock Status 2',
            'updated_at': '2023-12-26T13:00:00',
            'event_location': 'Mock Location 2',
            'participants': ['Participant 3', 'Participant 4'],
            'devices': ['Device 3', 'Device 4']
        }
    ]
    assert all(event in response.json['events'] for event in expected_events)

    # Optionally, you can check other properties of the response data as needed
    assert response.json['message'] == 'Success'

# Define a simple class to represent a mock event for testing purposes
class MockEvent:
    def __init__(self, id, event_title, event_type, start_time, end_time):
        self.id = id
        self.event_title = event_title
        self.event_type = event_type
        self.start_time = start_time
        self.end_time = end_time
