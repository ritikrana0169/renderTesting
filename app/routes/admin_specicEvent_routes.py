import re
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.routes.user_routes import role_required  
from app.services.admin_specificEvent_service import EventDetailsResource
from app.database import app
from app.models.model import db, Event 
from json import JSONEncoder 
from datetime import time


# from app.services.admin_addExternal_user_service import AdminExternalUserService
class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, time):
            return obj.strftime('%H:%M:%S')
        return super().default(obj)

# app = Flask(__name__)
app.json_encoder = CustomJSONEncoder  # Set custom JSON encoder

event_bp3 = Blueprint('event_bp3', __name__)  
# event_service = EventService() 

@event_bp3.route('/admin/event/<int:event_id>', methods=['GET'])
# @jwt_required()
# @role_required('Admin')
def get_events_for_user_by_userid(event_id):
    event_service = EventDetailsResource()
    events = event_service.get_events_for_user(event_id)
    return events

    # event_service = EventDetailsResource()
    # return jsonify({EventDetailsResource.get_events_for_user(event_id)})
    # try:
    #     events = event_service.get_events_for_user(event_id)
    #     if events:
    #         event_list = [
    #             {
    #                 'Event_Title': event.event_title,
    #                 'Event_Type': event.event_type,
    #                 'Event_Description': event.event_description,
    #                 'Event_Date': event.event_date,
    #                 'Start_Time': event.start_time.strftime('%H:%M:%S'),
    #                 'End_Time': event.end_time.strftime('%H:%M:%S'),
    #                 'created_at':event.created_at,
    #                 'event_status':event.event_status,
    #                 'updated_at':event.updated_at,
    #                 'event_location':event.event_location,
    #                 'participants':event.participants,
    #                 'devices':event.devices
    #             }
    #             for event in events
    #         ]
    #         # print(event_list)
    #         return jsonify({'events': event_list}), 200
    #     else:
    #         return jsonify({'message': 'No events found for the user'}), 404
    # except Exception as e:
    #     return jsonify({'message': str(e)}), 500