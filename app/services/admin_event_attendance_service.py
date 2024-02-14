from app.models.model import Event, Attendance, User, Device, db
from sqlalchemy import and_
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import jwt
from flask_bcrypt import check_password_hash

class Admineventservice:

    def get_event_attendance(self, event_id):
        """
        Get attendance details for a specific event, including present, late, and absent users.
        - For each user, checks attendance records on the event date.
        - Classifies users as present if check-in and check-out times fall within the event duration.
        - Classifies users as late if check-in occurs after 15 minutes of event start time.
        - Classifies users as absent if there's no attendance record or check-in/out times don't match event duration.
        """
        try:
            # Get the event
            event = Event.query.get(event_id)

            if event:
                # Get the list of users for the event
                event_users = event.participants

                # Initialize lists to store present, late, and absent users
                present_users = []
                late_users = []
                absent_users = []

                # Iterate through each user and check attendance
                for user in event_users:
                    # Check if there is attendance record for the user on the event date
                    attendance = Attendance.query.filter_by(user_id=user.id, date=event.event_date).first()

                    if attendance:
                        # Convert check-in time to datetime object
                        check_in_datetime = datetime.combine(event.event_date, attendance.check_in_time)

                        # Calculate the time difference from the event start and end time
                        time_difference_start = check_in_datetime - datetime.combine(event.event_date, event.start_time)
                        time_difference_end = check_in_datetime - datetime.combine(event.event_date, event.end_time)

                        # Check if user joined after 15 minutes from the event start time
                        if time_difference_start > timedelta(minutes=15):
                            # Check if user joined after the event end time
                            if time_difference_end > timedelta(minutes=0):
                                absent_users.append({'user_id': user.id, 'user_name': f'{user.first_name} {user.last_name}'})
                            else:
                                late_users.append({'user_id': user.id, 'user_name': f'{user.first_name} {user.last_name}'})
                        else:
                            present_users.append({'user_id': user.id, 'user_name': f'{user.first_name} {user.last_name}'})
                    else:
                        # If there is no attendance record, consider the user as absent
                        absent_users.append({'user_id': user.id, 'user_name': f'{user.first_name} {user.last_name}'})

                # Prepare the response
                response = {
                    'event_id': event.id,
                    'event_title': event.event_title,
                    'event_date': event.event_date.strftime('%Y-%m-%d'),
                    'start_time': event.start_time.strftime('%H:%M:%S'),
                    'end_time': event.end_time.strftime('%H:%M:%S'),
                    'present_users': present_users,
                    'late_users': late_users,
                    'absent_users': absent_users
                }

                return response, 200

            return {'error': 'Event not found'}, 404

        except Exception as e:
            return {'error': str(e)}, 500


    def get_user_activity(self, user_id):
        """
        Get the activity details for a specific user, including event participation and attendance status.
        - For each event the user participated in, checks attendance records on the event date.
        - Classifies user's attendance status based on check-in and check-out times.
        - Classifies user as present if check-in and check-out times fall within the event duration.
        - Classifies user as late if check-in occurs after 15 minutes of event start time.
        - Classifies user as absent if there's no attendance record or check-in/out times don't match event duration.
        """
        try:
            # Get the user
            user = User.query.get(user_id)

            if user:
                # Get the list of events for the user
                user_events = user.events

                # Initialize list to store user activity details
                user_activity = []

                # Iterate through each event and check user activity
                for event in user_events:
                    # Check if there is attendance record for the user on the event date
                    attendance = Attendance.query.filter_by(user_id=user.id, date=event.event_date).first()

                    if attendance:
                        # Convert check-in time to datetime object
                        check_in_datetime = datetime.combine(event.event_date, attendance.check_in_time)

                        # Calculate the time difference from the event start and end time
                        time_difference_start = check_in_datetime - datetime.combine(event.event_date, event.start_time)
                        time_difference_end = check_in_datetime - datetime.combine(event.event_date, event.end_time)

                        # Check user's attendance status based on check-in and check-out times
                        if time_difference_start > timedelta(minutes=15):
                            # Check if user joined after the event end time
                            if time_difference_end > timedelta(minutes=0):
                                status = 'Absent'
                            else:
                                status = 'Late'
                        else:
                            status = 'Present'
                    else:
                        status = 'Absent'

                    # Prepare event details
                    event_details = {
                        'event_id': event.id,
                        'event_title': event.event_title,
                        'event_date': event.event_date.strftime('%Y-%m-%d'),
                        'start_time': event.start_time.strftime('%H:%M:%S'),
                        'end_time': event.end_time.strftime('%H:%M:%S'),
                        'status': status
                    }

                    # Prepare user activity details
                    user_activity.append({
                        'user_id': user.id,
                        'user_name': f'{user.first_name} {user.last_name}',
                        'event_details': event_details
                    })

                if not user_activity:
                    return {'messaage': 'Not found any activity for this user'}, 404

                return user_activity, 200

            return {'error': 'User not found'}, 404

        except Exception as e:
            return {'error': str(e)}, 500


    def get_users_by_event_and_device(self, event_id, device_id):
        """
        Get users who attended a specific event using a particular device.
        """
        try:
            # Get the event
            event = Event.query.get(event_id)

            # Get the device
            device = Device.query.get(device_id)

            if event and device:
                # Get the list of users for the event
                event_users = event.participants

                # Get attendance records for the specified event and device
                attendance_records = Attendance.query.filter_by(device_id=device_id).all()

                # Extract user IDs from attendance records
                attended_user_ids = {record.user_id for record in attendance_records}

                # Filter users based on attendance records
                users_attended = [user for user in event_users if user.id in attended_user_ids]

                # Prepare the response
                response = {
                    'event_id': event.id,
                    'event_title': event.event_title,
                    'event_date': event.event_date.strftime('%Y-%m-%d'),
                    'start_time': event.start_time.strftime('%H:%M:%S'),
                    'end_time': event.end_time.strftime('%H:%M:%S'),
                    'device_id': device.id,
                    'users': [{'user_id': user.id, 'user_name': f'{user.first_name} {user.last_name}'} for user in users_attended]
                }

                return response, 200

            # Handle cases where event or device is not found
            if not event:
                return {'error': 'Event not found'}, 404
            if not device:
                return {'error': 'Device not found'}, 404

        except Exception as e:
            return {'error': str(e)}, 500
        
        
    def login_device(self, name, passcode):
        """
        Log in a device by verifying credentials, associating it with an event, and updating its status.
        """
        try:
            # Verify device credentials using name and passcode
            device = Device.query.filter_by(name=name).first()

            if device and check_password_hash(device.passcode, passcode):
                # Find the latest ongoing or upcoming event for the specific device on the current day
                event = self.get_latest_event(device.id)

                if event:
                    # Perform device login logic using simplified update_device_status
                    self.update_device_status(device, event)

                    # Generate JWT token
                    token_payload = {
                        'device_id': device.id,
                        'event_id': event.id,
                        'exp': datetime.utcnow() + timedelta(days=1)  # Token expiration time
                    }

                    # Load environment variables from .env file
                    load_dotenv()
                    secret_key = os.environ.get('JWT_SECRET_KEY')
                    jwt_token = jwt.encode(token_payload, secret_key, algorithm='HS256')

                    # Return the response
                    response = {
                        'token': jwt_token,
                        'event_id': event.id,
                        'device_id': device.id,
                        'event_type': event.event_type,
                        'event_name': event.event_title,
                        'device_location': device.location,
                        'message': 'Login successful'
                    }
                    return response, 200
                else:
                    return {'error': 'No events available for the device on the current day'}, 404
            else:
                return {'error': 'Invalid device credentials'}, 401

        except Exception as e:
            return {'error': str(e)}, 500

    def update_device_status(self, device, event):
        """
        Update the status of a device after successful login (simplified logic without last_login_at or events).
        """
        try:

            # Update device status to indicate that it is logged in
            device.availability = 'logged_in'


            # Commit changes to the database
            db.session.commit()

        except Exception as e:
            # Handle any exceptions that may occur during the device login process
            raise e

    def get_latest_event(self, device_id):
        """
        Get the latest ongoing or upcoming event for a specific device on the current day.
        """
        now = datetime.now().date()

        # Get events for the current day where the device is associated
        events = Event.query.filter(
            and_(
                Event.event_date == now,
                Event.devices.any(Device.id == device_id),
                Event.end_time > datetime.now().time()
            )
        ).order_by(Event.start_time).all()

        return events[0] if events else None   