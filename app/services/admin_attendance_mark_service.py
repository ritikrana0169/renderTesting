from app.models.model import db, Event, Device, User, Attendance
from datetime import datetime

def mark_attendance(identifier, event_id, device_id):
    print("Entered attendance function")
    try:
        # identifier = data.get('identifier')  # Use 'identifier' instead of 'userId'
        # event_id = data.get('eventId')
        # device_id = data.get('deviceId')

        # Check if both identifier, eventId, and deviceId are provided
        if not identifier or not event_id or not device_id:
            return {'error': 'identifier, eventId, and deviceId are required'}, 400

        # Check if the user, event, and device exist
        user = User.query.filter_by(identifier=identifier).first()
        if not user:
            return {'error': f'User with identifier {identifier} not found'}, 404

        event = Event.query.get(event_id)
        device = Device.query.get(device_id)

        if not event or not device:
            return {'error': 'Event or Device not found'}, 404

        # Check if the user is already marked as present for the event
        if user not in event.participants:
            return {'error': f'Warning: User with identifier {identifier} is not assigned to the event with id {event_id}'}, 400
        if device not in event.devices:
            return {'error': f'Warning: Device with id {device_id} is not assigned to the event with id {event_id}'}, 400

        # Check if attendance already exists for the same date, user, and event
        existing_attendance = Attendance.query.filter_by(
            date=datetime.now().date(),
            user_id=user.id,
            event_id=event.id,
        ).first()

        if existing_attendance:
            return {'error': 'User already marked as present for the event'}, 400

        # Mark attendance
        attendance = Attendance(
            date=datetime.now().date(),
            check_in_time=datetime.now().time(),
            status='Present',
            user_id=user.id,
            event_id=event.id,
            device_id=device.id,
        )

        db.session.add(attendance)
        db.session.commit()

        return {'message': 'Attendance marked successfully'}, 200

    except Exception as e:
        return {'error': str(e)}, 500


def get_events_attendance_history_by_user_role(user_role):
    try:
        # Get all events
        events = Event.query.all()

        # Prepare response data for each event based on user role
        response_data = []
        for event in events:
            # Get all users with the specified role assigned to the event
            users_with_role = [user for user in event.participants if user.role == user_role]

            # Get all attendances for the event and users with the specified role
            attendances = Attendance.query.filter(
                Attendance.event_id == event.id,
                Attendance.user_id.in_([user.id for user in users_with_role])
            ).all()

            # Calculate total, present, and absent users with the specified role
            total_users = len(users_with_role)
            present_users = len([attendance for attendance in attendances if attendance.status == 'Present'])
            absent_users = total_users - present_users

            # Prepare response for each event and user role
            event_data = {
                'event_title': event.event_title,
                'event_date': str(event.event_date),
                'total_users': total_users,
                'present_users': present_users,
                'absent_users': absent_users,
            
            }

            response_data.append(event_data)

        return response_data, 200

    except Exception as e:
        return {'error': str(e)}, 500