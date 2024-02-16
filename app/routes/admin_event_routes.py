import re

from flask_jwt_extended import jwt_required
from app.database import app
from flask import Blueprint, jsonify, request
from app.routes.user_routes import role_required  
from app.services.admin_event_service import EventService
from json import JSONEncoder
from app.models.model import db, Event
from datetime import time
from app.services.admin_event_service import EventService


# from app.services.admin_addExternal_user_service import AdminExternalUserService


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, time):
            return obj.strftime('%H:%M:%S')
        return super().default(obj)


# app = Flask(__name__)
app.json_encoder = CustomJSONEncoder  # Set custom JSON encoder

addExternaluser_blueprint = Blueprint('addExternaluser_blueprint', __name__)

event_bp = Blueprint('event_bp', __name__)
all_event_bp = Blueprint('allevents_bp', __name__)
event_service = EventService()


# Getting all events  
@all_event_bp.route('/get_allevents', methods=['GET'])  
# @jwt_required()
# @role_required('Admin')
def get_events_for_user_by_userid():
    event_service = EventService()
    try:
        # events = event_service.get_events_for_user()
        events = event_service.get_all_events()
        if events:
            event_list = [
                {
                    'id': event.id,
                    'event_title': event.event_title,
                    'event_type': event.event_type,
                    'event_description': event.event_description,
                    'event_date': event.event_date,
                    'start_time': event.start_time.strftime('%H:%M:%S'),
                    'end_time': event.end_time.strftime('%H:%M:%S'),
                    'created_at': event.created_at,
                    'event_status': event.event_status,
                    'updated_at': event.updated_at,
                    'event_location': event.event_location,
                    'participants': event.participants,
                    'devices': event.devices

                }
                for event in events
            ]
            print(event_list)
            return jsonify({'events': event_list}), 200
        else:
            return jsonify({'message': 'No events found for the user'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500


# Update event details
@event_bp.route('/admin/events/<int:event_id>', methods=['PUT'])
# @jwt_required()
# @role_required('Admin')
def update_event(event_id):
    # Get updated data from request
    data = request.get_json()

    # Update event using the EventService
    event = event_service.update_event(event_id, data)

    updated_event = {
        'id': event.id,
        'event_title': event.event_title,
        'event_type': event.event_type,
        'event_description': event.event_description,
        'event_date': event.event_date,
        'start_time': event.start_time.strftime('%H:%M:%S'),
        'end_time': event.end_time.strftime('%H:%M:%S'),
        'created_at': event.created_at,
        'event_status': event.event_status,
        'updated_at': event.updated_at,
        'event_location': event.event_location
    }

    if updated_event:
        return jsonify({'message': 'Event updated successfully', 'event': updated_event}), 200
    else:
        return jsonify({'error': 'Event not found'}), 404


# Delete an event
@event_bp.route('/admin/events/<int:event_id>', methods=['DELETE'])
# @jwt_required()
# @role_required('Admin')
def delete_event(event_id):
    deleted = event_service.delete_event(event_id)

    if deleted:
        return jsonify({'message': 'Event deleted successfully'}), 200
    else:
        return jsonify({'error': 'Event not found'}), 404


@event_bp.route('/admin/events', methods=['GET'])
# @jwt_required()
# @role_required('Admin')
def get_events_by_type():
    # Get query parameters
    event_type = request.args.get('type')
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    # Call the service method to get events
    response_data = EventService.get_events_by_type(event_type, page, per_page)

    return jsonify({"data": response_data}), 200

    # Endpoint to search for users participating in a specific event by their first name or last name.


@event_bp.route('/admin/events/<int:event_id>/user', methods=['GET'])
# @jwt_required()
# @role_required('Admin')
def search_users_in_event(event_id):
    try:
        search_query = request.args.get('search', '')
        users_data = EventService.search_users_in_event(event_id, search_query)
        return jsonify(users_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
