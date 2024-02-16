# admin_user_route.py
import re
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.routes.user_routes import role_required
from app.services.admin_getEventDetailsById_service import Get_event_by_EventId
from app.exception.admin_externalUser_exception import EventException, UserException, GenericException
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.routes.user_routes import role_required

GetEvent_blueprint = Blueprint('GetEvent_blueprint', __name__)
@GetEvent_blueprint.route('/event/<int:event_id>', methods=['GET'])
# @jwt_required()
# @role_required('Admin')
def get_event_by_EventId_endpoint(event_id):
    try:
        guestList = Get_event_by_EventId.get_event_by_EventId_endpoint(event_id)
        return jsonify(guestList)
        
    except (EventException, UserException, GenericException) as e:
        return e.to_response()

