from flask import Flask, Blueprint, jsonify, request
from app.models.model import User, Event, Device, Attendance
from app.services.admin_attendance_mark_service import mark_attendance, get_events_attendance_history_by_user_role

event_userAttendance_mark = Blueprint('event_userAttendance_mark', __name__)

# @event_userAttendance_mark.route('/admin/mark_attendance', methods=['POST'])
def mark_attendance_route(identifier, event_id, device_id):
    # data = request.get_json()
    # identifier = data.get('identifier')
    # event_id = data.get('eventId')
    # device_id = data.get('deviceId')

    # Check if both identifier, eventId, and deviceId are provided
    if not identifier or not event_id or not device_id:
        return {'error': 'identifier, eventId, and deviceId are required'}, 400

    # Check if the user with the specified identifier exists
    user = User.query.filter_by(identifier=identifier).first()

    if user:
        # Proceed only if the user is found
        data['userId'] = user.id
        result, status_code = mark_attendance(data)
        return jsonify(result), status_code
    else:
        return {'error': f'User with identifier {identifier} not found'}, 404


@event_userAttendance_mark.route('/admin/allevent_attedance_history/<string:user_role>', methods=['GET'])
def get_attendance_history(user_role):
    try:
        response_data = get_events_attendance_history_by_user_role(user_role)
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
