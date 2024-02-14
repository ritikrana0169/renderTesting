from flask import Blueprint, jsonify, request
from app.services.qrCodeScannerService import check_qrcode_scanned

qrCodeScanner_routes = Blueprint('qrCodeScanner_routes', __name__)

@qrCodeScanner_routes.route('/scanned/qrcode', methods=['POST'])
def check_qrcode_scanned_route():
    try:
        data = request.get_json()
        qr_identifier = data.get('qr_identifier')
        device_id = data.get('device_id')  # Add this line to extract device_id

        if qr_identifier is None or device_id is None:
            return jsonify({'error': 'Invalid request data. Please provide the right data'}), 400

        result = check_qrcode_scanned(qr_identifier, device_id)  # Pass device_id to the function
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
