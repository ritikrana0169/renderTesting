
from flask import Flask, request, jsonify
from app.models.model import db, Event,RepeatDay,repeat_days_events
from datetime import datetime
from app.exception.admin_externalUser_exception import EventException, GenericException

class CreateEventResource:
    def newEvent(data):
        existing_event = Event.query.filter_by(
            event_title=data['event_title'].strip(),
            event_date=data['event_date'],
            event_location=data['event_location'],
            start_time=data['start_time'],
            event_type=data['event_type']
        ).first()

        if existing_event:
            raise EventException('An event with similar details already exists')

        # Create a new event
        new_event = Event(
            event_title=data['event_title'].strip(),
            event_type=data['event_type'],
            event_description=data['event_description'],
            event_date=datetime.strptime(data['event_date'], '%Y-%m-%d').date(),
            start_time=datetime.strptime(data['start_time'], '%H:%M:%S').time(),
            end_time=datetime.strptime(data['end_time'], '%H:%M:%S').time(),
            event_status='Upcoming',
            event_location=data['event_location'],
            repeat_type=data['repeat_type']
        )

        # Add repeat days to the event
        if data['repeat_type']=='Daily':
            data['repeat_days']= ["monday", "tuesday","wednesday","thursday", "friday", "saturday","sunday"]
        repeat_days = data.get('repeat_days', [])
        for day in repeat_days:
            repeat_day = RepeatDay.query.filter_by(day=day.lower()).first()
            if repeat_day:
                new_event.repeat_days.append(repeat_day)
        try:
        # Save the event to the database
            db.session.add(new_event)
            db.session.commit()
            event_data ={'event_id': new_event.id, 
                'event_title': new_event.event_title, 
                'event_type': new_event.event_type, 
                'event_description': new_event.event_description,
                'event_date': new_event.event_date,
                'start_time': data['start_time'],
                'end_time': data['end_time'],
                'event_status': new_event.event_status,
                'event_location': new_event.event_location,
                'repeat_type': new_event.repeat_type,
                'repeat_days':repeat_days
            }
            
            return event_data
        except Exception as e:
            # Handle other exceptions
            db.session.rollback()
            raise GenericException(str(e))


