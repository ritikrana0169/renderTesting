
# app.routes.admin_event_routes.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.routes.user_routes import role_required
from app.services.admin_event_attendance_service import Admineventservice
 

admin_event_attendance_routes = Blueprint('admin_event_attendance_routes', __name__)
admineventservice = Admineventservice()

@admin_event_attendance_routes.route('/admin/events/<int:event_id>/attendance', methods=['GET'])
# @jwt_required()
# @role_required('Admin')
def get_event_attendance(event_id):
    result, status_code = admineventservice.get_event_attendance(event_id)
    return jsonify(result), status_code


@admin_event_attendance_routes.route('/admin/user/activity/<int:user_id>', methods=['GET'])
# @jwt_required()
# @role_required('Admin')
def get_user_activity(user_id):
    result, status_code = admineventservice.get_user_activity(user_id)
    return jsonify(result), status_code

@admin_event_attendance_routes.route('/admin/events/<int:event_id>/devices/<int:device_id>/users', methods=['GET'])
# @jwt_required()
# @role_required('Admin')
def get_users_by_event_and_device(event_id, device_id):
    result, status_code = admineventservice.get_users_by_event_and_device(event_id, device_id)
    return jsonify(result), status_code

@admin_event_attendance_routes.route('/api/admin/device/login', methods=['POST'])
# @jwt_required()
# @role_required('Admin') 
def device_login():
    try:
        # Validate request payload
        data = request.get_json()
        name = data.get('name')
        passcode = data.get('passcode')

        if not name or not passcode:
            return jsonify({'error': 'name and passcode are required'}), 400

        # Call the login_device method from Admineventservice
        response, status_code = admineventservice.login_device(name, passcode)

        return jsonify(response), status_code

    except Exception as e:
        return jsonify({'error': str(e)}), 500