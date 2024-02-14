 # admin_user_route.py
import re
from flask import Blueprint, request, jsonify
from app.services.all_attendance_history_of_organization_service import Allevent_attedance_history_service
from app.exception.admin_externalUser_exception import OrganizationException, GenericException


Allevent_attedance_history_blueprint = Blueprint('Allevent_attedance_history_blueprint', __name__)

    
@Allevent_attedance_history_blueprint.route('/allevent_attedance_history', methods=['GET'])
def get_allevent_attedance_history():
    try:
        attedance = Allevent_attedance_history_service.allevent_attedance_history()
        response_message = {
            "data":attedance
    },200
        return response_message
        
    except (OrganizationException, GenericException) as e:
        return e.to_response()