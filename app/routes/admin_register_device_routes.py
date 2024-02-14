from flask import Blueprint, request, jsonify
from app.services.admin_register_device_service import AdminDeviceService
from app.exception.eventDeviceExecption import DeviceException, GenericException
# import ipaddress
from app.services.admin_register_device_service import get_registered_devices

device_routes = Blueprint('devices', __name__)


@device_routes.route('/admin/device', methods=['POST'])
def add_new_device():
    """
    Endpoint to add a new device.
    Request JSON format:
    {
      "name": "DeviceName",
      "ip_address": "192.168.1.1",
      "location": "Some Location",
      "availability": "Available",
      "passcode": "DevicePasscode"
    }
    """
    try:
        # Get data from the request
        data = request.get_json()

        # Validate the request data
        if 'name' not in data or not data['name']:
            return jsonify({'error': 'Device name is required'}), 400

        if 'ip_address' not in data or not data['ip_address']:
            return jsonify({'error': 'IP address is required'}), 400

        # Validate IP address format (you can uncomment this block if needed)
        # if not is_valid_ip(data['ip_address']):
        #     return jsonify({'error': 'Invalid IP address format'}), 400

        if 'location' not in data or not data['location']:
            return jsonify({'error': 'Location is required'}), 400

        if 'availability' not in data or data['availability'].lower() not in ['available', 'unavailable']:
            return jsonify({'error': 'Availability must be either "Available" or "Unavailable"'}), 400

        if 'passcode' not in data or not data['passcode']:
            return jsonify({'error': 'Passcode is required'}), 400

        # Call the service to add the new device
        response = AdminDeviceService.add_new_device(data)

        return response

    except Exception as e:
        # Handle exceptions and return an error response
        return jsonify({'error': str(e)}), 500


@device_routes.route('/admin/device/<int:device_id>', methods=['PUT'])
def update_device(device_id):
    """
    {
      "name": "UpdatedDeviceName",
      "ip_address": "Updated 192.168.1.1",
      "location": "Updated Location"
    }
    """

    # Validate the request data
    # if 'name' not in data or not data['name']:
    #     return jsonify({'error': 'Device name is required'}), 400
    #
    # if 'ip_address' not in data or not data['ip_address']:
    #     return jsonify({'error': 'IP address is required'}), 400
    #
    # if 'location' not in data or not data['location']:
    #     return jsonify({'error': 'Location is required'}), 400
    try:
        # Get data from the request
        data = request.get_json()

        # Validate the request data
        if not data:
            return jsonify({'error': 'No data provided for update'}), 400

        # Validate the availability field
        if 'availability' in data and data['availability'].lower() not in ['available', 'unavailable']:
            return jsonify({'error': 'Availability must be either "Available" or "Unavailable"'}), 400

        response = AdminDeviceService.update_device(device_id, data)
        return response

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


@device_routes.route('/admin/device/<int:device_id>', methods=['DELETE'])
def remove_device_endpoint(device_id):
    try:
        response = AdminDeviceService.remove_device(device_id)
        return response

    except (DeviceException, GenericException) as e:
        return e.to_response()


@device_routes.route('/admin/devices', methods=['GET'])
def get_devices():
    try:
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)
        devices = get_registered_devices(page=page, per_page=per_page)
        return jsonify({'devices': devices})

    except Exception as e:
        return jsonify({'error': str(e)})

# def is_valid_ip(ip):
#     try:
#         # Try to create an IPv4 or IPv6 address object
#         ip_obj = ipaddress.ip_address(ip)
#         return True
#     except ValueError:
#         # ValueError is raised for an invalid IP address format
#         return False
