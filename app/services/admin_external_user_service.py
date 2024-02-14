# admin_user_service.py
from flask import jsonify
from app.models.model import User, db, Event,user_events
from sqlalchemy import select
from app.exception.admin_externalUser_exception import EventException, UserException, GenericException

class AdminExternalUserService:
    @staticmethod
    def add_external_user(data,event_id):
        # Check if the user already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            raise UserException('User already exists.')
        event = Event.query.get(event_id)
        if(event == None):
            raise EventException(f'Event not found with event id: {event_id}')

        # Create a new external user instance
        new_user = User(
            role="Guest",
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone=data['phone'],
            gender=data['gender'],
            status='Active'
        )

        try:
            # Add the new user to the database
            event.participants.append(new_user)
            db.session.add(new_user)
            db.session.commit()
            guests_data ={
                'user_id': new_user.id, 
                'first_name': new_user.first_name, 
                'last_name': new_user.last_name, 
                'email': new_user.email,
                'phone': new_user.phone,
                'gender': new_user.gender,
                'status': new_user.status,
                'role':new_user.role
            }
            return guests_data
        except Exception as e:
            # Handle other exceptions
            db.session.rollback()
            raise GenericException(str(e))

    #done
    @staticmethod
    def remove_external_user(event_id, id):
        
        user = User.query.get(id)
        if(user == None or user.role !='Guest'):
            # return jsonify({'message': 'Guest not found'}), 400
            raise UserException(f'Inviled user id : {id}')
        event = Event.query.get(event_id)
        
        if(event == None):
            # return jsonify({'message': 'event not found'}), 400
            raise EventException(f'Event not found with event id: {event_id}')
        
        eventList = user.events
        if len(eventList) == 0:
            # return jsonify({'message': 'Guest not registered with event'}), 400
            raise UserException(f'No guest found with event id : {event_id}')

        for e in eventList:
            if(e.id==event_id):
                break
            else:
                # return jsonify({'message': 'Guest not registered with event'}), 400
                raise UserException(f'No guest found with event id : {event_id}')

        try:
            # if event and user:
            user.events.remove(event)
            # db.session.delete(user)
            db.session.commit()
            return {'message': 'User successfully removed.'}, 200
        except Exception as e:
            # Handle other exceptions
            db.session.rollback()
            raise GenericException(str(e))

        
    
    def get_external_user_byEventId(event_id,page,per_page):

        offset = (page - 1) * per_page
        event = Event.query.get(event_id)
        if(event == None):
            raise EventException(f'Event not found with event id: {event_id}')     

        # guestsList = event.participants
        # guests = [i for i in guestsList if i.role == 'Guest']
        guests=User.query.filter(User.role == 'Guest').offset(offset).limit(per_page).all()
        guests_data = [
            {'user_id': guest.id, 
            'first_name': guest.first_name, 
            'last_name': guest.last_name, 
            'email': guest.email,
            'phone': guest.phone,
            'gender': guest.gender,
            'status': guest.status}
            for guest in guests
        ]
        if len(guests_data) == 0:
            raise UserException(f'No guest found with event id :{event_id}')
        else:
            return guests_data

    @staticmethod
    def add_external_users(data,event_id):
        # Checking the event exists or not
        event = Event.query.get(event_id)
        # Checking if the user already exists
        if(event == None):
            raise EventException(f'Event not found with event id: {event_id}')
        for d in data:
            existing_user = User.query.filter_by(email=d['email']).first()
            if existing_user:
                raise UserException(f"User already exists with email {d['email']} ")


        try:
            guests_data=[]
            # Create a new external user instance
            for user_data in data:
                new_user = User(
                    role="Guest",
                    first_name=user_data['first_name'].strip(),
                    last_name=user_data['last_name'].strip() ,
                    email=user_data['email'],
                    phone=user_data['phone'],
                    gender=user_data['gender'],
                    status='Active'
                )
                db.session.add(new_user)
                event.participants.append(new_user)
                db.session.commit()
                guests_data.append({
                    'user_id': new_user.id, 
                    'first_name': new_user.first_name, 
                    'last_name': new_user.last_name, 
                    'email': new_user.email,
                    'phone': new_user.phone,
                    'gender': new_user.gender,
                    'status': new_user.status,
                    'role':new_user.role
                })

            return guests_data
        except Exception as e:
            # Handle other exceptions
            db.session.rollback()
            raise GenericException(str(e))