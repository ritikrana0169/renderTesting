import os
from app.models.model import Image, User
from app.models.model import User, db
from flask import jsonify
import re
from app.models.model import User, db
from app.models.model import Event
from datetime import datetime
import random
import string
from flask_bcrypt import check_password_hash, generate_password_hash

# creating a class EventService
# This calss will have a function to fetch all events of user by user_id
# With the help of userId, we verify that the user exist or not, if user is present
# in database it will return the events, alse throw error.
class EventService:
    def get_events_for_user(self, user_id):
        user = User.query.get(user_id)

        try:
            if user:
                # print(user.events)
                return user.events
            else:
                return jsonify({'message': 'User not found1'})
        except Exception as e:
            return jsonify({'message': 'User not found2'}), 404

          
          

    def get_upcoming_events_for_user(self, user_id):
        current_datetime = datetime.now()

        user = User.query.get(user_id)
        try:
            if user:
                upcoming_events = [
                    event for event in user.events
                    if event.event_date > current_datetime.date() or (
                            event.event_date == current_datetime.date() and event.start_time >= current_datetime.time()
                    )
                ]
                # print(upcoming_events)
                return upcoming_events
            else:
                return jsonify({'message': 'User not found'})
        except Exception as e:
            return jsonify({'message': 'User not found'}), 404




    def get_completed_events_for_user(self, user_id):
        current_datetime = datetime.now()

        user = User.query.get(user_id)
        try:
            if user:
                completed_events = [
                    event for event in user.events
                    if event.event_date < current_datetime.date() or (
                            event.event_date == current_datetime.date() and event.end_time < current_datetime.time()
                    )
                ]
                return completed_events
            else:
                return jsonify({'message': 'User not found'})
        except Exception as e:
            return jsonify({'message': 'User not found'}), 404



    def get_active_events_for_user(self, user_id):
        current_datetime = datetime.now()

        user = User.query.get(user_id)

        try:
            if user:
                active_events = [
                    event for event in user.events
                    if (
                            event.event_date == current_datetime.date()
                            and event.start_time <= current_datetime.time() <= event.end_time
                    )
                ]
                return active_events
            else:
                return jsonify({'message': 'User not found'})
        except Exception as e:
            return jsonify({'message': 'User not found'}), 404



    def get_event_by_id(self, event_id):
        try:
            event = Event.query.get(event_id)

            if event:
                event_data = {
                    'Event_Id': event.id,
                    'Event_Title': event.event_title,
                    'Event_Type': event.event_type,
                    'Event_Desc': event.event_description,
                    'Event_Venue': event.event_location,
                    'Event_Date': event.event_date.strftime('%Y-%m-%d'),
                    'Start_Time': event.start_time.strftime('%H:%M:%S'),
                    'End_Time': event.end_time.strftime('%H:%M:%S'),
                }
                return jsonify({'event': event_data})
            else:
                return jsonify({'message': 'Event not found'}), 404
        except Exception as e:
            return jsonify({'message': 'Something went wrong'}), 500




# User service class
class UserService:

    # code of update user data
    @staticmethod
    def update_user(user_id, new_data):
        # Retrieve the user from the database
        user = User.query.get(user_id)
    
        if not user:
            raise ValueError("User not found")
    
        # Exclude fields that should not be updated
        excluded_fields = ['status', 'identifier', 'id', 'password', 'role']
    
        # Check if any excluded fields are present in new_data
        invalid_fields = [field for field in excluded_fields if field in new_data]
        if invalid_fields:
            raise ValueError(f"Cannot update the following fields: {', '.join(invalid_fields)}")
    
        # Validate and update user data
        for key, value in new_data.items():
            # Validate specific fields if needed
            if key == 'email' and not UserService.is_valid_email(value):
                raise ValueError("Invalid email format")
            elif key == 'phone' and not UserService.is_valid_phone(value):
                raise ValueError("Invalid phone format")
    
            # Update user data
            setattr(user, key, value)
    
        # Update the 'updated_at' field
        user.updated_at = datetime.utcnow()
    
        # Commit the changes to the database
        db.session.commit()
        return user

    @staticmethod
    def get_user_by_id(user_id):
        try:
            # Check if the user exists
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404

            organization_data = {}
            if user.organization:
                organization_data = {
                    'organization_id': user.organization.id,
                    'org_name': user.organization.org_name,
                    'org_type': user.organization.org_type,
                    'address': user.organization.address,
                    'contact_email': user.organization.contact_email,
                    'contact_phone': user.organization.contact_phone,
                    'status': user.organization.status,
                }

            user_data = {
                'id': user.id,
                'identifier': user.identifier,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'address': user.address,
                'gender': user.gender,
                'organization': organization_data
            }

            return jsonify({'user': user_data}), 200
        except Exception as ex:
            return jsonify({'error': f'An error occurred: {str(ex)}'}), 500





    # validation methods
    @staticmethod
    def is_valid_email(email):
        # Basic email format validation using regular expression
        email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        return bool(re.match(email_pattern, email))

    @staticmethod
    def is_valid_phone(phone):
        # Basic phone format validation using regular expression
        phone_pattern = re.compile(r'^\d{10}$')
        return bool(re.match(phone_pattern, phone))

    # validation methods ends here
    

    # code of upload user image 
    @staticmethod
    def add_image_to_user(user_id, file_paths):
        try:
            # Create new Image instances and associate them with the user
            for file_path in file_paths:
                new_image = Image(user_id=user_id, url=file_path)
                db.session.add(new_image)

            # Commit all changes to the database
            db.session.commit()
        except Exception as e:
            # Handle database errors
            db.session.rollback()
            raise ValueError(f'Error adding image(s) to user: {str(e)}')

    @staticmethod
    def generate_unique_filename(user_id, original_filename):
        # Generate a unique filename based on timestamp, user ID, and a random component
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=3))
        user = User.query.get(user_id)
        return f"{user.identifier}_{random_string}.{original_filename.split('.')[-1]}"

    @staticmethod
    def save_image(user_id, upload_folder, img):
        try:
            # Generate a unique filename
            filename = UserService.generate_unique_filename(user_id, img.filename)

            # Construct the full file path
            filepath = os.path.join(upload_folder, filename)

            # Save the image
            img.save(filepath)

            return filepath
        except Exception as e:
            # Handle file-saving errors
            raise ValueError(f'Error saving image: {str(e)}')

            

    # code of change password
    # code of change password
    @staticmethod
    def change_user_password(user_id, current_password, new_password, confirm_new_password):
        # Retrieve the user from the database
        user = User.query.get(user_id)
    
        if not user:
            raise ValueError("User not found")
    
        # Validate the current password
        if not check_password_hash(user.password, current_password):
            raise ValueError("Invalid current password")
    
        # Validate the new password
        if not UserService.is_valid_password(new_password):
            raise ValueError("Password: 8+ chars, 1 uppercase, 1 lowercase, 1 digit.")
    
        # Check if the new password matches the confirmation
        if new_password != confirm_new_password:
            raise ValueError("New password and confirmation do not match")
    
        # Hash and update the password
        hashed_password = generate_password_hash(new_password).decode('utf-8')
        user.password = hashed_password
    
        # Update the 'updated_at' field
        user.updated_at = datetime.utcnow()
    
        # Commit the changes to the database
        db.session.commit()
    
        return jsonify({"message": "Password changed successfully"}), 200
        
    @staticmethod  
    def is_valid_password(password):
       # Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter,
       # one digit, and one special character (including dot '.').
       password_pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.])[A-Za-z\d@$!%*?&.]{8,}$')
       return bool(re.match(password_pattern, password))


#Hashing the password of the user
#Class method to fetch the user by email

