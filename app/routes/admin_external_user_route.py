# admin_user_route.py
import re
from flask import Blueprint, request, jsonify
from app.services.admin_external_user_service import AdminExternalUserService
from app.exception.admin_externalUser_exception import EventException, UserException, GenericException
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.routes.user_routes import role_required

Externaluser_blueprint = Blueprint('Externaluser_blueprint', __name__)


@Externaluser_blueprint.route('/events/<int:event_id>/add_external_user', methods=['POST'])
# @jwt_required()
# @role_required('Admin')
def add_external_user(event_id):
    """ POST request data
        {
            "first_name": "abc",
            "last_name": "xyz",
            "email": "demo@gmail.com",
            "phone": "7634567890",
            "gender":"Male"
        }
    """
    # Get data from the request
    data = request.get_json()

    if 'email' not in data or not is_valid_email(data['email']):
        return jsonify({'message': 'Invalid email format'}), 404

    if 'phone' not in data or not is_valid_mobile_number(data['phone']):
        return jsonify({'message': 'Invalid phone no.'}), 404
    
    if 'gender' not in data or data['gender'] not in ['Male', 'Female']:
        return jsonify({'message': 'Invalid gender'}), 404
    
    try:
        response = AdminExternalUserService.add_external_user(data,event_id)
        response_message = {
            "data":response,
            "message":"User added successfully"  
        },201
        return response_message

    except (EventException, UserException, GenericException) as e:
        return e.to_response()

def is_valid_email(email):
    # Regular expression for a valid email address
    email_pattern = re.compile(r'^\S+@\S+\.\S+$')
    return bool(re.match(email_pattern, email))

def is_valid_mobile_number(phone):
    # Define a regular expression pattern for a mobile number starting with 6-9
    pattern = re.compile(r'^[6-9]\d{9}$')

    # Check if the mobile number matches the pattern
    match = re.match(pattern, phone)

    return bool(match)


@Externaluser_blueprint.route('/events/<int:event_id>/external_user/<int:id>', methods=['DELETE'])
# @jwt_required()
# @role_required('Admin')
def remove_external_user_endpoint(event_id, id):
    try:
        response = AdminExternalUserService.remove_external_user(event_id,id)
        return response
    
    except (EventException, UserException, GenericException) as e:
        return e.to_response()
    
@Externaluser_blueprint.route('/events/<int:event_id>/external_user', methods=['GET'])
# @jwt_required()
# @role_required('Admin')
def get_external_user_byEventId_endpoint(event_id):
    try:
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)
        guestList = AdminExternalUserService.get_external_user_byEventId(event_id,page,per_page)
        return jsonify(guestList)
        
    except (EventException, UserException, GenericException) as e:
        return e.to_response()
    


@Externaluser_blueprint.route('/events/<int:event_id>/add_external_users', methods=['POST'])
# @jwt_required()
# @role_required('Admin')
def add_external_users(event_id):
    """ POST request data
        {
            "first_name": "abc",
            "last_name": "xyz",
            "email": "demo@gmail.com",
            "phone": "7634567890",
            "gender":"Male"
        }
    """
    # Get data from the request

    getdata = request.get_json()
    data=getdata['data']
    for d in data:
        if 'email' not in d or not is_valid_email(d['email']):
            return jsonify({'message': f'Invalid email format {d["email"]}'}), 404
        if 'phone' not in d or not is_valid_mobile_number(d['phone']):
            return jsonify({'message': f'Invalid phone no.{d["phone"]}'}), 404
        if 'gender' not in d or d['gender'].lower() not in ['male', 'female']:
            return jsonify({'message': f'Invalid gender {d["gender"]}'}), 404

    
    try:
        response = AdminExternalUserService.add_external_users(data,event_id)
        response_message = {
            "data":response,
            "message":"User added successfully"  
        },201
        return response_message

    except (EventException, UserException, GenericException) as e:
        return e.to_response()

