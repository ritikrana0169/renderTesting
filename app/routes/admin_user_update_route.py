import re

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.routes.user_routes import role_required
from app.services.admin_user_update_service import AdminUserUpdateService

update_users_blueprint = Blueprint('updateuser', __name__)


@update_users_blueprint.route('/admin/users/<int:user_id>', methods=['PUT'])
# @jwt_required()
# @role_required('Admin')
def update_user(user_id):
    """ PUT request data
        {
            "email": "jane@gmail.com",
            "phone": "1234567890",
            "gender": "Male",
            "status": "Inactive"
        }
    """

    # Get data from the request
    data = request.get_json()

    # Validate the request data
    if 'email' in data and not is_valid_email(data['email']):
        return jsonify({'error': 'Invalid email format, email should be in ----@gmail.com format'}), 400

    if 'phone' not in data or not is_valid_phone(data['phone']):
        return jsonify({'error': 'Invalid phone number format'}), 400
    
    if 'gender' not in data or data['gender'] not in ['Male', 'Female', 'Other']:
        return jsonify({'error': 'Invalid gender, gender should be Male, Female or Other'}), 400

    if 'status' in data and data['status'] not in ['Active', 'Inactive']:
        return jsonify({'error': 'Invalid status, status should be Active or Inactive'}), 400

    response = AdminUserUpdateService.update_user(user_id, data)
    return response


def is_valid_email(email):
    # Regular expression for a valid email address
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@gmail.com$')
    return bool(re.match(email_pattern, email))


def is_valid_password(password):
    # Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter,
    # one digit, and one special character (including dot '.').
    password_pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.])[A-Za-z\d@$!%*?&.]{8,}$')
    return bool(re.match(password_pattern, password))


def is_valid_phone(phone_number):
    # Phone number pattern allowing for various formats
    phone_pattern = re.compile(r'^\+?[1-9]\d{9,14}$')
    return bool(re.match(phone_pattern, phone_number))
