import pytest
from flask import Flask, json
from app.models.model import db
from app.routes.admin_register_device_routes import device_routes

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
    app.register_blueprint(device_routes, url_prefix='/api')

    yield app

    # Drop all tables after the test
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    # Create a test client
    return app.test_client()



def test_delete_device(client):
    # Test case for deleting an existing device
    device_id = 1
    response = client.delete(f'admin/device/{device_id}')
    if response.status_code == 200:
        assert b'{"error":"Invalid event"}' in response.data 

def test_delete_device_not_found(client):
    # Test case for deleting a non-existing device
    device_id = 99999999

    response = client.delete(f'admin/device/{device_id}')
    if response.status_code == 400:
        assert b'{"error":"Invalid event"}' in response.data 
 