from flask import jsonify

def UserException(message="User not found", status_code=404):
    return jsonify(message=message), status_code


def AdminException(message="Admin not found", status_code=404):
    return jsonify(message=message), status_code


def OrganizationException(message="Organization not found", status_code=404):
    return jsonify(message=message), status_code


def EventException(message="Event not found", status_code=404):
    return jsonify(message=message), status_code


def QRCodeException(message="QRCode not found", status_code=404):
    return jsonify(message=message), status_code

def FaceRecognizationException(message="Face not Recognized", status_code=404):
    return jsonify(message=message), status_code

def AttendenceException(message="Attendence not saved", status_code=404):
    return jsonify(message=message), status_code

def DeviceException(message="Device not found", status_code=404):
    return jsonify(message=message), status_code

def ImageException(message="Image not saved", status_code=404):
    return jsonify(message=message), status_code

def EmailException(message="Not able to send Email", status_code=404):
    return jsonify(message=message), status_code