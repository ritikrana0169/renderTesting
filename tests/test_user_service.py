import json
import unittest
from urllib.parse import quote
from flask import Flask
from app.models.model import db, User
from app.routes.user_routes import user_update  # Assuming user_update is your blueprint
from app.services.user_services import UserService
from app.services.admin_user_service import AdminUserService
from flask_bcrypt import Bcrypt

class UserServicesTestCase(unittest.TestCase):

    def setUp(self):
        # Set up a test Flask app
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/db'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        # Create a test client
        self.client = self.app.test_client()

        # Bind SQLAlchemy to the app
        db.init_app(self.app)

        # Create all tables
        with self.app.app_context():
            db.create_all()

            # Create a sample user in the database
            sample_user_data = {
                "identifier": "asd123",
                "first_name": "Yash",
                "last_name": "Thakur",
                "role": "User",
                "email": "rajt49300@gmail.com",
                "phone": "1234567890",
                "address":"Indore",
                "password": "Masai@123",
                "status": "Active",
                "gender":"Male"
            }
            AdminUserService.add_user(sample_user_data)

        # Register the user blueprint
        self.app.register_blueprint(user_update)

    def tearDown(self):
        # Clean up the database after each test
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_update_user(self):
        # Update the user's information
        updated_data = {
            "first_name": "UpdatedRaj",
            "last_name": "UpdatedThakur",
            "email": "updated.raj@gmail.com",
            "phone": "7898785236",
            "address": "Pune"
            # Include fields that can be updated
        }

        response_update = self.client.put('/updateUser/1',
                                          data=json.dumps(updated_data), content_type='application/json')

        self.assertEqual(response_update.status_code, 200)
        self.assertIn(b"User updated successfully", response_update.data)

        # Retrieve the updated user from the database
        with self.app.app_context():
            updated_user = db.session.query(User).filter_by(id=1).first()

        # Assertions to check if the user is updated correctly
        self.assertEqual(updated_user.first_name, "UpdatedRaj")
        self.assertEqual(updated_user.last_name, "UpdatedThakur")
        self.assertEqual(updated_user.email, "updated.raj@gmail.com")
        self.assertEqual(updated_user.phone, "7898785236")
        self.assertEqual(updated_user.address, "Pune")

        # Add more assertions as needed

    def test_change_user_password(self):
        # Change the user's password
        change_password_data = {
            "current_password": "Masai@123",
            "new_password": "NewMasai@456",
            "confirm_new_password": "NewMasai@456"
        }

        response_change_password = self.client.put('/changePassword/1',
                                                  data=json.dumps(change_password_data), content_type='application/json')

        self.assertEqual(response_change_password.status_code, 200)
        self.assertIn(b"Password changed successfully", response_change_password.data)

        # Retrieve the updated user from the database
        with self.app.app_context():
            updated_user = db.session.query(User).filter_by(id=1).first()

        # Assertions to check if the password is changed correctly
        bcrypt = Bcrypt(self.app)
        self.assertTrue(bcrypt.check_password_hash(updated_user.password, "NewMasai@456"))

        # Add more assertions as needed

if __name__ == '__main__':
    unittest.main()
