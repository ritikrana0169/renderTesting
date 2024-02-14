# eventDeviceException.py

from flask import jsonify

class EventException(Exception):
    def __init__(self, message="Event not found", status_code=404):
        self.message = message
        self.status_code = status_code
        super().__init__()

    def to_response(self):
        return jsonify(message=self.message), self.status_code


class DeviceException(Exception):
    def __init__(self, message="Device not found", status_code=404):
        self.message = message
        self.status_code = status_code
        super().__init__()

    def to_response(self):
        return jsonify(message=self.message), self.status_code


class GenericException(Exception):
    def __init__(self, message="Internal Server Error", status_code=500):
        self.message = message
        self.status_code = status_code
        super().__init__()

    def to_response(self):
        return jsonify(message=self.message), self.status_code
