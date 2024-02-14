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


def test_get_external_users_for_event_success(client):
    # Assuming event_id=1 exists and has associated external users in your test database
    event_id=1
    response = client.get(f'admin/events/{event_id}/external_user')

    if response.status_code == 400:
        assert b'{"error":"Invalid event"}' in response.data 

def test_get_external_users_for_nonexistent_event(client):
    # Assuming event_id=999 does not exist in your test database
    event_id=999
    response = client.get(f'admin/events/{event_id}/external_user')

    if response.status_code == 400:
        assert b'{"error":"Invalid event"}' in response.data 

def test_get_external_users_for_event_no_associations(client):
    # Assuming event_id=2 exists but has no associated external users in your test database
    event_id=2
    response = client.get(f'admin/events/{event_id}/external_user')

    if response.status_code == 400:
        assert b'{"error":"No any externalUser in this event"}' in response.data 

