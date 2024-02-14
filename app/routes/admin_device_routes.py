# eventDeviceRoutes.py

from flask import Flask, Blueprint, jsonify, request
from app.models.model import db
from app.services.admin_device_service import admin_eventdevice_servic
from app.exception.eventDeviceExecption import EventException, DeviceException, GenericException

eventDevice_routes = Blueprint('eventDevice_routes', __name__)

@eventDevice_routes.route('/admin/events/<int:event_id>/add_device/<int:device_id>', methods=['POST'])
def add_device_to_event_endpoint(event_id, device_id):
    try:
        result = admin_eventdevice_servic.add_device_to_event(event_id, device_id)
        return jsonify(result)

    except (EventException, DeviceException, GenericException) as e:
        return e.to_response()

@eventDevice_routes.route('/admin/events/<int:event_id>/devices', methods=['GET'])
def get_devices_for_event_endpoint(event_id):
    try:
        devices = admin_eventdevice_servic.get_devices_for_event(event_id)

        if devices is not None:
            return jsonify(devices)
        else:
            return jsonify({'error': 'Event not found'}), 404

    except (EventException, GenericException) as e:
        return e.to_response()

@eventDevice_routes.route('/admin/events/<int:event_id>/add_device/<int:device_id>', methods=['DELETE'])
def remove_device_from_event_endpoint(event_id, device_id):
    try:
        result = admin_eventdevice_servic.remove_device_from_event(event_id, device_id)
        return jsonify(result)

    except (EventException, DeviceException, GenericException) as e:
        return e.to_response()
