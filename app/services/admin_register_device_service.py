# admin_register_device_service.py
from flask import jsonify
from app.models.model import Device, db
from app.exception.eventDeviceExecption import DeviceException, GenericException
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


class AdminDeviceService:
    @staticmethod
    def add_new_device(data):
        try:
            # Check if a device with the same name, IP address, and location already exists
            existing_device = Device.query.filter_by(
                name=data['name'],
                ip_address=data['ip_address'],
                location=data['location']
            ).first()

            if existing_device:
                return jsonify({'error': 'Device with the same name, IP address, and location already exists'}), 400

            # Hash the passcode
            hashed_passcode = bcrypt.generate_password_hash(data['passcode']).decode('utf-8')

            # Create a new device instance
            new_device = Device(
                name=data['name'],
                ip_address=data['ip_address'],
                location=data['location'],
                availability=data['availability'],
                passcode=hashed_passcode  # Store the hashed passcode in the database
            )

            # Add the new device to the database
            db.session.add(new_device)
            db.session.commit()

            # Return the device id with a success message in the response
            return jsonify({'message': 'Device added successfully', 'id': new_device.id}), 201
        except Exception as e:
            # Handle other exceptions and rollback the session in case of an error
            db.session.rollback()
            return jsonify({'error': f'An error occurred: {str(e)}'}), 500

    @staticmethod
    def update_device(device_id, data):
        try:
            # Check if the device with device_id exists
            existing_device = Device.query.get(device_id)
            if not existing_device:
                return jsonify({'error': 'Device not found'}), 404

            # Update the device details based on the provided data
            for key, value in data.items():
                if key == 'passcode':
                    return jsonify({'error': 'Password update not allowed'}), 400

                if hasattr(existing_device, key):
                    setattr(existing_device, key, value)

            # Commit the changes to the database
            db.session.commit()

            return jsonify(
                {
                    'message': 'Device updated successfully',
                    'device': {"name": existing_device.name, "ip_address": existing_device.ip_address,
                               "location": existing_device.location}
                }), 200
        except Exception as e:
            # Handle other exceptions
            db.session.rollback()
            return jsonify({'error': f'An error occurred: {str(e)}'}), 500

    @staticmethod
    def remove_device(device_id):
        device = Device.query.get(device_id)

        if (device == None):
            raise DeviceException(f'Device not found with device id: {device_id}')

        try:
            # if device:
            db.session.delete(device)
            # db.session.delete(device)
            db.session.commit()
            return {'message': 'Device successfully removed.'}, 200
        except Exception as e:
            # Handle other exceptions
            db.session.rollback()
            raise GenericException(str(e))


def get_registered_devices(page=1, per_page=10):
    try:
        devices = Device.query.paginate(page=page, per_page=per_page, error_out=False)

        if not devices:
            raise Exception("No devices found.")
        device_list = []

        for device in devices:
            device_info = {
                'id': device.id,
                'name': device.name,
                'ip_address': device.ip_address,
                'location': device.location,
                'availability': device.availability
            }
            device_list.append(device_info)

        return device_list

    except Exception as e:
        raise Exception(f"Error fetching devices: {str(e)}")
