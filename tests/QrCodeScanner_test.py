import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, json
from app.routes.qrCodeScanner_routes import check_qrcode_scanned_route


class TestQRCodeScannerRoutes(unittest.TestCase):
    def setUp(self):
        # Set up a test Flask app
        self.app = Flask(__name__)

    def tearDown(self):
        pass

    @patch('app.routes.qrCodeScanner_routes.check_qrcode_scanned')
    def test_check_qrcode_scanned_route_valid_qr_identifier(self, mock_check_qrcode_scanned):
        # Mock the check_qrcode_scanned function to avoid actual database operations
        mock_check_qrcode_scanned.return_value = {'message': 'QR code for user John scanned.'}

        # Send a POST request to the route with the provided valid QR identifier
        with self.app.test_request_context('/qr/scanned/qrcode', json={
            'qr_identifier': 'gAAAAABljSQgH19tdtqamHLyVaUbkHB4_ThR3JGSKIDomIGHivF8_nSkONqdrmTr-ZO-9NM1nwdmnQC09W0YqrSgkbY6pXa1og=='}):
            response = check_qrcode_scanned_route()

        # Assert that the response status code is 200 and contains the expected message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'QR code for user John scanned. Now, you can join the event.'})

        # Assert that the check_qrcode_scanned function was called with the correct argument
        mock_check_qrcode_scanned.assert_called_once_with(
            'gAAAAABljSQgH19tdtqamHLyVaUbkHB4_ThR3JGSKIDomIGHivF8_nSkONqdrmTr-ZO-9NM1nwdmnQC09W0YqrSgkbY6pXa1og==')

    def test_check_qrcode_scanned_route_invalid_qr_identifier(self):
        # Send a POST request to the route with an invalid QR identifier
        with self.app.test_request_context('/qr/scanned/qrcode', json={'qr_identifier': None}):
            response = check_qrcode_scanned_route()

        # Assert that the response status code is 400 and contains the expected error message
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'error': 'Invalid request data please provide right data'})


if __name__ == '__main__':
    unittest.main()
