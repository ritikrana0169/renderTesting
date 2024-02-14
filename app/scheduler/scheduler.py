from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from flask import Flask
from app.database import db
from app.models.model import Event

def check_event_status():
    with app.app_context():
        now = datetime.now().time()
        update_device_availability_for_inactive_events()  

def update_device_availability_for_inactive_events():
    try:
        # Query all inactive events
        inactive_events = Event.query.filter_by(event_status='Inactive').all()

        if inactive_events:
            for event in inactive_events:
                # Check if there are devices assigned to the inactive event
                if event.devices:
                    for device in event.devices:
                        # Update device availability to 'Unavailable'
                        device.availability = 'Aavailable'

            # Commit the changes to the database
            db.session.commit()
            return {'message': 'Device availability updated for all devices in inactive events.'}, 200
        else:
            return {'message': 'No inactive events found.'}, 404
    except Exception as e:
        return {'error': str(e)}, 500
def initialize_scheduler(app_instance):
    global app
    app = app_instance

    scheduler = BackgroundScheduler()
    scheduler.add_job(check_event_status, 'interval', seconds=50)  # Check every 30 seconds
    scheduler.start()
