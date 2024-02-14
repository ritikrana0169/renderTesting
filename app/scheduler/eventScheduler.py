from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from flask import Flask
from app.database import db
from app.models.model import Event

def check_event_status():
    with app.app_context():
        now = datetime.now().time()
        upcoming_events = Event.query.filter(Event.start_time <= now,Event.end_time > now,Event.event_date <= datetime.now().date(), Event.event_status == 'Upcoming').all()
        if upcoming_events:
            for event in upcoming_events:
                if(event.event_type =='Once'):
                    if(event.event_date==datetime.now().date()):
                        event.event_status = 'Active'
                        # print(f"Event '{event.event_title}' is now Active!")
                else:
                    event.event_status = 'Active'
                # print(f"Event '{event.event_title}' is now active!")
            # Commit changes to the database
            db.session.commit()

        events_to_end = Event.query.filter(Event.end_time <= now, Event.event_status == 'Active').all()
        for event in events_to_end:
            if(event.event_type =='Once'):
                event.event_status='Inactive'
                # print(f"Event '{event.event_title}' is now Inactive!")
            else:
                event.event_status = 'Upcoming'
                # print(f"Event '{event.event_title}' is now Upcoming!")
            db.session.commit()

def initialize_scheduler(app_instance):
    global app
    app = app_instance

    scheduler = BackgroundScheduler()
    scheduler.add_job(check_event_status, 'interval', seconds=30)  # Check every 30 seconds
    scheduler.start()
