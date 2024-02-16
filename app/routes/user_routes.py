from functools import wraps
import os
from flask import Flask, jsonify, Blueprint, abort, current_app, request
from json import JSONEncoder
from urllib.parse import quote
from app.database import app
from app.services.user_services import EventService
from app.models.model import db, User, Image, Organization
from datetime import time, datetime
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity,JWTManager
from app.services.user_services import UserService
from flask_cors import CORS
# from app.exceptions.exception import UserException
from flask_bcrypt import check_password_hash
# from app.DA.train import trainservice





#method for securing routes according to roles
def role_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            current_user_roles = get_jwt_identity().get('roles', [])

            if any(role in current_user_roles for role in roles):
                return fn(*args, **kwargs)
            else:
                return jsonify(msg='Access denied'), 403

        return decorator
    return wrapper


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, time):
            return obj.strftime('%H:%M:%S')
        return super().default(obj)

app.json_encoder = CustomJSONEncoder  # Set custom JSON encoder


# creating blueprint for get_allevents_of_user route
events_blueprint = Blueprint('events', __name__)
@events_blueprint.route('/get_allevents_of_user/<int:user_id>', methods=['GET'])
@jwt_required()
@role_required('User')
def get_events_for_user_by_userid(user_id):
    """
        Get all events for a specific user by user ID.

        Parameters:
        - user_id (int): User ID for whom events are requested.

        Returns:
        - JSON response containing events information.
        """
    event_service = EventService()
    try:
        events = event_service.get_events_for_user(user_id)
        if events:
            event_list = [
                {
                    'Event_Id': event.id,
                    'Event_Title': event.event_title,
                    'Event_Type': event.event_type,
                    'Event_Desc': event.event_description,
                    'Event_Venue': event.event_location,
                    'Event_Date': event.event_date.strftime('%Y-%m-%d'),
                    'Start_Time': event.start_time.strftime('%H:%M:%S'),
                    'End_Time': event.end_time.strftime('%H:%M:%S'),
                }
                for event in events
            ]
            return jsonify({'events': event_list}), 200
        else:
            return jsonify({'message': 'No events found for the user'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500




@events_blueprint.route('/get_upcoming_eventsOf_user/<int:user_id>', methods=['GET'])
@jwt_required()
@role_required('User')
def get_upcoming_events_for_user(user_id):
    """
        Get upcoming events for a specific user by user ID.

        Parameters:
        - user_id (int): User ID for whom upcoming events are requested.

        Returns:
        - JSON response containing upcoming events information.
        """
    event_service = EventService()
    try:
        upcoming_events = event_service.get_upcoming_events_for_user(user_id)
        if upcoming_events:
            event_list = [
                {
                    'Event_Id': event.id,
                    'Event_Title': event.event_title,
                    'Event_Type': event.event_type,
                    'Event_Desc': event.event_description,
                    'Event_Venue': event.event_location,
                    'Event_Date': event.event_date.strftime('%Y-%m-%d'),
                    'Start_Time': event.start_time.strftime('%H:%M:%S'),
                    'End_Time': event.end_time.strftime('%H:%M:%S'),
                }
                for event in upcoming_events
            ]
            return jsonify({'upcoming_events': event_list}), 200
        else:
            return jsonify({'message': 'No upcoming events for the user'}), 404
    except Exception as e:
        return jsonify({'message': 'something went wrong'}), 500





@events_blueprint.route('/get_completed_events_of_user/<int:user_id>', methods=['GET'])
@jwt_required()
@role_required('User')
def get_completed_events_for_user(user_id):
    """
        Get completed events for a specific user by user ID.

        Parameters:
        - user_id (int): User ID for whom completed events are requested.

        Returns:
        - JSON response containing completed events information.
        """
    event_service = EventService()
    try:
        completed_events = event_service.get_completed_events_for_user(user_id)
        if completed_events:
            event_list = [
                {
                    'Event_Id': event.id,
                    'Event_Title': event.event_title,
                    'Event_Type': event.event_type,
                    'Event_Desc': event.event_description,
                    'Event_Venue': event.event_location,
                    'Event_Date': event.event_date.strftime('%Y-%m-%d'),
                    'Start_Time': event.start_time.strftime('%H:%M:%S'),
                    'End_Time': event.end_time.strftime('%H:%M:%S'),
                }
                for event in completed_events
            ]
            return jsonify({'completed_events': event_list}), 200
        else:
            return jsonify({'message': 'No completed events for the user'}), 404
    except Exception as e:
        return jsonify({'message': 'Something went wrong'}), 500





@events_blueprint.route('/get_active_events_of_user/<int:user_id>', methods=['GET'])
# @jwt_required()
# @role_required('User')
def get_active_events_for_user(user_id):
    """
        Get active events for a specific user by user ID.

        Parameters:
        - user_id (int): User ID for whom active events are requested.

        Returns:
        - JSON response containing active events information.
        """
    event_service = EventService()
    try:
        active_events = event_service.get_active_events_for_user(user_id)

        if active_events:
            event_list = [
                {
                    'Event_Id': event.id,
                    'Event_Title': event.event_title,
                    'Event_Type': event.event_type,
                    'Event_Desc': event.event_description,
                    'Event_Venue': event.event_location,
                    'Event_Date': event.event_date.strftime('%Y-%m-%d'),
                    'Start_Time': event.start_time.strftime('%H:%M:%S'),
                    'End_Time': event.end_time.strftime('%H:%M:%S'),
                }
                for event in active_events
            ]
            return jsonify({'active_events': event_list})
        else:
            return jsonify({'message': 'No active events for the user'}), 404
    except Exception as e:
        return jsonify({'message': 'Something went wrong'}), 500






@events_blueprint.route('/get_event/<int:event_id>', methods=['GET'])

def get_event(event_id):
    """
        Get details of a specific event by event ID.

        Parameters:
        - event_id (int): Event ID for which details are requested.

        Returns:
        - JSON response containing event details.
        """
    event_service = EventService()
    try:
        result = event_service.get_event_by_id(event_id)
        return result, 200
    except Exception as e:
        return jsonify({'message': 'Something went wrong'}), 500




      
#creating blueprint for login auth
auth_bp = Blueprint("auth", __name__)

#creating JWT manager
jwt = JWTManager()
 
#route for user login
from datetime import timedelta
from flask_jwt_extended import create_access_token, create_refresh_token

@auth_bp.post("/login")
def login_user():
    data = request.get_json()

    user = User.query.filter_by(email=data.get("email")).first()

    if user and check_password_hash(user.password, data.get("password")):
        roles = [user.role]
        access_token = create_access_token(
            identity={
                "user_id": user.id,
                "user_email": user.email,
                "roles": roles
            },
            expires_delta=timedelta(minutes=720)  # Set the access token expiry to 12 Hours
        )
        refresh_token = create_refresh_token(
            identity={
                "user_id": user.id,
                "user_email": user.email,
                "roles": user.role
            },
            expires_delta=timedelta(minutes=840)  # Set the refresh token expiry to 14 Hours
        )

        return jsonify({
            "message": "Logged In ",
            "tokens": {"access": access_token, "refresh": refresh_token},
            "user_id": user.id,
            "user_role": user.role
        }), 201

    return jsonify({"error": "Invalid username or password"}), 401



#route for refreshing token
@auth_bp.get("/refresh")
@jwt_required(refresh=True)
def refresh_access():
    identity = get_jwt_identity()

    new_access_token = create_access_token(identity=identity)

    return jsonify({"access_token": new_access_token})

# JWT error handlers
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    return jsonify({"message": "Token has expired", "error": "token_expired"}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify({"message": "Signature verification failed", "error": "invalid_token"}),
        401,
    )

@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify({
            "message": "Request doesn't contain a valid token",
            "error": "authorization_header",
        }),
        401,
    )


#creating blueprint of upload user details
user_update = Blueprint("userUpdate", __name__)

# route of update user
@user_update.route('/updateUser/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    try:
        updated_user = UserService.update_user(user_id, data)
        return jsonify({"message": "User updated successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    

# image upload endpoint
@user_update.route('/uploadImages/<int:user_id>', methods=['POST'])
def upload_images(user_id):
    try:
        # Check if the 'images' field is present in the form data
        if 'images' not in request.files:
            return jsonify({'error': 'No images found in the form data'}), 400

        # Check if there are any files attached to the 'images' field
        images = request.files.getlist('images')
        if not images or all(img.filename == '' for img in images):
            return jsonify({'error': 'No valid images found in the form data'}), 400

        # Check if the user exists
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Check if the user is associated with an organization
        organization = user.organization
        if not organization:
            return jsonify({'error': 'User is not associated with any organization'}), 400

        # Ensure the 'TrainingImages' folder exists
        base_folder = 'TrainingImages'
        os.makedirs(base_folder, exist_ok=True)

        # Ensure the organization folder exists inside 'TrainingImages'
        organization_folder = os.path.join(base_folder, f'{organization.id}_{organization.org_name}')
        os.makedirs(organization_folder, exist_ok=True)

        # Process each image
        file_paths = [UserService.save_image(user_id, organization_folder, img) for img in images]

        # Add the images to the user in the database
        UserService.add_image_to_user(user_id, file_paths)
        # calling the DA function
        # trainservice.trainfolder(organization_folder)

        return jsonify({'message': 'Images uploaded successfully'}), 201
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


# route of change password
@user_update.route('/changePassword/<int:user_id>', methods=['PUT'])
def change_user_password(user_id):
    data = request.get_json()
    try:
        response = UserService.change_user_password(user_id, data.get('current_password'), data.get('new_password'), data.get('confirm_new_password'))
        return response
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# route to get user images
@user_update.route('/getUserImages/<int:user_id>', methods=['GET'])
def get_user_images(user_id):
    try:
        # Check if the user exists
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Retrieve user images
        user_images = Image.query.filter_by(user_id=user_id).all()

        # Replace backslashes with forward slashes in image URLs
        image_urls = [img.url.replace("\\", "/") for img in user_images]

        return jsonify({'user_id': user_id, 'image_urls': image_urls}), 200

    except Exception as e:
        # Handle unexpected errors
        return jsonify({'error': f'Error retrieving user images: {str(e)}'}), 500






user_details_bp = Blueprint('user_details', __name__)
@user_details_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """ 
        Get details of a specific user by user ID.
 
        Parameters:
        - user_id (int): User ID for whom details are requested.

        Returns:
        - JSON response containing user details.
        """
    # Validate for user_id
    if not isinstance(user_id, int) or user_id <= 0:
        return jsonify({'error': 'Invalid user ID'}), 400

    response = UserService.get_user_by_id(user_id)
    return response






