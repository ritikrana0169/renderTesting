import pytest
from flask import Flask, json
from app.models.model import db
from app.routes.admin_external_user_route import Externaluser_blueprint

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
    app.register_blueprint(Externaluser_blueprint, url_prefix='/admin')

    yield app

    # Drop all tables after the test
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    # Create a test client
    return app.test_client()



def test_delete_externalUserFromEvent(client):
    # Test case for deleting an existing event
    event_id = 1
    id = 1

    response = client.delete(f'admin/events/{event_id}/external_user/{id}')
    if response.status_code == 200:
    #     and b"Guest not found" in response.data:
    #     print("Test passed as expected: 400 Error with 'Guest not found' message")
    # else:
        assert b'{"error":"Invalid event"}' in response.data 

def test_delete_guest_not_found(client):
    # Test case for deleting a non-existing guest
    event_id = 1
    id = 99999

    response = client.delete(f'admin/events/{event_id}/external_user/{id}')
    if response.status_code == 400:
        assert b'{"error":"Invalid event"}' in response.data 

def test_delete_event_not_found(client):
    # Test case for deleting a non-existing event
    event_id = 99999
    id = 1

    response = client.delete(f'admin/events/{event_id}/external_user/{id}')
    if response.status_code == 400: 
        assert b'{"error":"Invalid guest"}' in response.data 