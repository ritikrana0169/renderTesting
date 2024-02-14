import pytest
from flask import Flask, json
from app.models.model import db, Event, Device,User
from app.services.admin_device_service import admin_eventdevice_servic
from app.routes.admin_device_routes import eventDevice_routes
from app.routes.admin_eventUser_routes import eventUser_routes


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
    app.register_blueprint(eventDevice_routes, url_prefix='/eventDevice')
    app.register_blueprint(eventUser_routes, url_prefix='/eventUser')

    yield app

    # Drop all tables after the test
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    # Create a test client
    return app.test_client()


# test case :1) # Adding a user to an event who is not already present
def test_add_user_in_event(client):
    with client.application.app_context():
       event = Event(event_title='Test Event', event_type='Test Type')
       user = User(first_name = "Johon",last_name="mohta",address="delhi")
    #    print(client)
       
       db.session.add(event)
       db.session.add(user)
       db.session.commit()

       response = client.post('/eventUser/admin/events/{}/add_user/{}'.format(event.id,user.id))
       assert response.status_code == 200
       assert b'{"Event_Title":"Test Event","Event_Type":"Test Type","User":"Johonmohta","message":"User add successfully"}' in response.data


# # test case :2) # Here I am adding the user to the event who is already present
def test_add_user_in_event_allrady(client):
    with client.application.app_context():
       event = Event(event_title='Test Event', event_type='Test Type')
       user = User(first_name = "Johon",last_name="mohta",address="delhi")
    #    print(client)
       
       db.session.add(event)
       db.session.add(user)
       event.participants.append(user)
       db.session.commit()

       response = client.post('/eventUser/admin/events/{}/add_user/{}'.format(event.id,user.id))
       assert response.status_code == 404
       assert b'{"Event_Title":"Test Event","Event_Type":"Test Type","User":"Johonmohta","message":"User allredy prsent in the event"}' in response.data


# # test case :3) # Here I am geting all user of the event
def test_get_all_user_of_event(client):
    with client.application.app_context():
       event = Event(event_title='Test Event', event_type='Test Type')
       user = User(first_name = "Johon",last_name="mohta",address="delhi")
    #    print(client)
       
       db.session.add(event)
       db.session.add(user)
       event.participants.append(user)
       db.session.commit()

       response = client.get('/eventUser/admin/events/{}/user'.format(event.id))
       assert response.status_code == 200
       user_data = response.get_json()
       assert len(user_data) == 5


# # test case :4) # Here I am geting all user of a event but any user dose not exist in the event
def test_get_all_user_of_event_but_not_present(client):
    with client.application.app_context():
       event = Event(event_title='Test Event', event_type='Test Type')

       db.session.add(event)
       db.session.commit()

       response = client.get('/eventUser/admin/events/{}/user'.format(event.id))
       assert response.status_code == 404
       user_data = response.get_json()
       assert len(user_data) == 4


# test case :5) # Here I am deleting a user of the event
def test_delete_user_from_event(client):
    with client.application.app_context():
       event = Event(event_title='Test Event', event_type='Test Type')
       user = User(first_name = "Johon",last_name="mohta",address="delhi")
       
       db.session.add(event)
       db.session.add(user)
       event.participants.append(user)
       db.session.commit()

       response = client.delete('eventUser/admin/events/{}/user/{}'.format(event.id,user.id))
       assert response.status_code == 200
       assert b'{"Event_Title":"Test Event","Event_Type":"Test Type","User":"Johonmohta","message":"User deleted successfully"}' in response.data


# test case :6) # Here I am deleting a user of a event but user not exist
def test_delete_user_from_event_but_user_not_exist(client):
    with client.application.app_context():
       event = Event(event_title='Test Event', event_type='Test Type')
       user = User(first_name = "Johon",last_name="mohta",address="delhi")

       db.session.add(event)
       db.session.commit()

       response = client.delete('eventUser/admin/events/{}/user/{}'.format(event.id,1))
       assert response.status_code == 404
       assert b'{"message":"User not found"}' in response.data

# test case :7) # Here I am adding many users in the event.
def test_add_many_in_event(client):
    with client.application.app_context():
       event = Event(id = 1,event_title='Test Event', event_type='Test Type')
       user1 = User(id = 1,first_name = "Johon",last_name="mohta",address="delhi")
       user2 = User(id = 2,first_name = "mohan",last_name="disha",address="mumbai")

       data = [user1.id,user2.id]

       db.session.add(event)
       db.session.add(user1)
       db.session.add(user2)
       db.session.commit()

       response = client.post('eventUser/admin/events/{}/add_many_users'.format(event.id), data=json.dumps(data), content_type='application/json')
       assert response.status_code == 200
       assert b'{"Event_Title":"Test Event","Event_Type":"Test Type","add status list":["User add successfully with 1 id","User add successfully with 2 id"],"message":"2 User added"}' in response.data

# test case :8) # Here I am adding many users in the event but users are already present in the event.
def test_add_many_in_event_but_users_already_present(client):
    with client.application.app_context():
       event = Event(id = 1,event_title='Test Event', event_type='Test Type')
       user1 = User(id = 1,first_name = "Johon",last_name="mohta",address="delhi")
       user2 = User(id = 2,first_name = "mohan",last_name="disha",address="mumbai")

       data = [user1.id,user2.id]

       db.session.add(event)
       db.session.add(user1)
       db.session.add(user2)
       event.participants.append(user1)
       event.participants.append(user2)
       db.session.commit()

       response = client.post('eventUser/admin/events/{}/add_many_users'.format(event.id), data=json.dumps(data), content_type='application/json')
       assert response.status_code == 404
       assert b'{"Event_Title":"Test Event","Event_Type":"Test Type","add status list":["User allredy prsent in the event with 1 id","User allredy prsent in the event with 2 id"],"message":"0 User added"}' in response.data
       

# test case :9) # Here I am deleting many users from the event.
def test_delete_many_users_from_event(client):
    with client.application.app_context():
       event = Event(id = 1,event_title='Test Event', event_type='Test Type')
       user1 = User(id = 1,first_name = "Johon",last_name="mohta",address="delhi")
       user2 = User(id = 2,first_name = "mohan",last_name="disha",address="mumbai")

       data = [user1.id,user2.id]

       db.session.add(event)
       db.session.add(user1)
       db.session.add(user2)
       event.participants.append(user1)
       event.participants.append(user2)
       db.session.commit()

       response = client.delete('eventUser/admin/events/{}/delete_many_users'.format(event.id), data=json.dumps(data), content_type='application/json')
       assert response.status_code == 200
       assert b'{"Event_Title":"Test Event","Event_Type":"Test Type","delete status list":["User deleted successfully with 1 id, Johon mohta","User deleted successfully with 2 id, mohan disha"],"message":"2 User deleted"}' in response.data
    

# test case :10) # Here I am deleting many users from the event but users are not present in the event.
def test_delete_many_users_from_event_but_users_not_exist(client):
    with client.application.app_context():
       event = Event(id = 1,event_title='Test Event', event_type='Test Type')
       user1 = User(id = 1,first_name = "Johon",last_name="mohta",address="delhi")
       user2 = User(id = 2,first_name = "mohan",last_name="disha",address="mumbai")

       data = [user1.id,user2.id]

       db.session.add(event)
       db.session.add(user1)
       db.session.add(user2)
       db.session.commit()

       response = client.delete('eventUser/admin/events/{}/delete_many_users'.format(event.id), data=json.dumps(data), content_type='application/json')
       assert response.status_code == 404
       assert b'{"Event_Title":"Test Event","Event_Type":"Test Type","delete status list":["User is not in event with 1 id, Johon mohta","User is not in event with 2 id, mohan disha"],"message":"0 User deleted"}' in response.data
       