from flask import jsonify

from app.models.model import User, db


class AdminUserUpdateService:
    @staticmethod
    def update_user(user_id, data):
        # Check if the user exists
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Update user details
        if 'phone' in data:
            user.phone = data['phone']
        if 'email' in data:
            user.email = data['email']
        if 'gender' in data:
            user.gender = data['gender']
        if 'status' in data:
            user.status = data['status']

        try:
            db.session.commit()
            return jsonify({'message': 'User details updated successfully'}), 200
        except Exception as e:  # Handle other exceptions
            db.session.rollback()
            return jsonify({'error': f'An error occurred: {str(e)}'}), 500

