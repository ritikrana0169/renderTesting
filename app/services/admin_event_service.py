from app.models.model import db, Event, User

from datetime import datetime
from flask import jsonify
from sqlalchemy import asc


class EventService:

    # Method to get all events
    def get_all_events(self):
        return Event.query.all()

    def update_event(self, event_id, data):
        event = Event.query.get(event_id)

        if not event:
            return None  # Event not found            

        # Update event details
        event.start_time = data.get('start_time', event.start_time)
        event.end_time = data.get('end_time', event.end_time)
        event.event_title = data.get('event_title', event.event_title)
        event.event_type = data.get('event_type', event.event_type)
        event.event_description = data.get('event_description', event.event_description)
        event.event_status = data.get('event_status', event.event_status)
        event.event_date = data.get('event_date', event.event_date)
        event.event_location = data.get('event_location', event.event_location)
        db.session.commit()

        return event

    # Method to delete an event by ID
    def delete_event(self, event_id):
        event = Event.query.get(event_id)

        if not event:
            return False  # Event not found

        # Delete the event from the database
        db.session.delete(event)
        db.session.commit()

        return True  # Event deleted successfully    

    @staticmethod
    # Method to get all the events by type and according to page
    def get_events_by_type(event_type, page=1, per_page=10):

        # Get the current date and time
        current_datetime = datetime.now()

        # Initialize an empty list to store response data
        events = []

        # Get events by type with pagination
        if event_type == 'upcoming':
            events = Event.query.filter(
                (Event.event_date > current_datetime.date()) |
                ((Event.event_date == current_datetime.date()) & (Event.start_time > current_datetime.time()))
            ).order_by(asc(Event.event_date), asc(Event.start_time)).paginate(page=page, per_page=per_page,
                                                                              error_out=False)

        elif event_type == 'live':
            events = Event.query.filter(
                (Event.event_date == current_datetime.date()) &
                (Event.start_time <= current_datetime.time()) &
                (Event.end_time >= current_datetime.time())
            ).order_by(asc(Event.event_date), asc(Event.start_time)).paginate(page=page, per_page=per_page,
                                                                              error_out=False)

        elif event_type == 'completed':
            events = Event.query.filter(
                (Event.event_date < current_datetime.date()) |
                ((Event.event_date == current_datetime.date()) & (Event.end_time < current_datetime.time()))
            ).order_by(asc(Event.event_date), asc(Event.start_time)).paginate(page=page, per_page=per_page,
                                                                              error_out=False)

        else:
            # No specific event type specified, fetch all events
            events = Event.query.order_by(asc(Event.event_date), asc(Event.start_time)).paginate(page=page,
                                                                                                 per_page=per_page,
                                                                                                 error_out=False)

        # Prepare response data
        response_data = []
        for event in events.items:
            response_data.append({
                'id': event.id,
                'title': event.event_title,
                'type': event.event_type,
                'description': event.event_description,
                'date': event.event_date.isoformat(),
                'start_time': event.start_time.isoformat(),
                'end_time': event.end_time.isoformat(),
                'status': event.event_status,
                'location': event.event_location,
                'created_at': event.created_at,
                'updated_at': event.updated_at,
                # 'users':event.participants
            })

        return response_data

    @staticmethod
    def search_users_in_event(event_id, search_query):
        try:
            event = Event.query.get(event_id)
            if not event:
                return {'message': 'Event not found.'}

            users_in_event = event.participants
            if search_query:
                users_in_event = User.query.filter(
                    (User.first_name.ilike(f'%{search_query}%')) | (User.last_name.ilike(f'%{search_query}%')),
                    User.id.in_([user.id for user in users_in_event])
                ).all()

            if not users_in_event:
                return {'message': 'No users found in the event.'}

            users_data = [{
                'id': user.id,
                'identifier': user.identifier,
                'role': user.role,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'address': user.address,
                'email': user.email,
                'phone': user.phone,
                'status': user.status,
                'gender': user.gender
            } for user in users_in_event]

            return users_data
        except Exception as e:
            raise Exception(f'An error occurred: {str(e)}')
