import pytest
from flask import Flask
from app.models.model import db
from app.routes.all_attendance_history_of_organization_route import Allevent_attedance_history_blueprint

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
    app.register_blueprint(Allevent_attedance_history_blueprint, url_prefix='/admin')

    yield app

    # Drop all tables after the test
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    # Create a test client
    return app.test_client()



def test_get_allevent_attedance_history(client):
    response = client.delete(f'allevent_attedance_history ')
    if response.status_code == 200:
        assert b'{"message":"Successful"}' in response.data 
