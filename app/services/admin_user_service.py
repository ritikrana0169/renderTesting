# admin_user_service.py
from flask import jsonify
import qrcode
from app.models.model import Attendance, User, db, QRCode
from app.services.admin_email_service_for_registered_users import send_welcome_email
from flask_bcrypt import Bcrypt
from sqlalchemy import or_
from fuzzywuzzy import process

bcrypt = Bcrypt()


class AdminUserService:

    @staticmethod
    def get_all_users():
        try:
            # Query all users from the database
            users = User.query.all()
            return users
        except Exception as e:
            # Handle other exceptions
            return f'An error occurred: {str(e)}'

    @staticmethod
    def get_paginated_users(page=1, per_page=10):
        try:
            # Query paginated users from the database
            users_pagination = User.query.paginate(page=page, per_page=per_page, error_out=False)

            if not users_pagination.items:
                raise Exception("No users found.")

            users = users_pagination.items
            users_data = []

            for user in users:
                user_info = {
                    'id': user.id,
                    'identifier': user.identifier,
                    'role': user.role,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'address': user.address,
                    'email': user.email,
                    'phone': user.phone,
                    'status': user.status,
                    'gender': user.gender,
                    'created_at': user.created_at,
                    'updated_at': user.updated_at if user.updated_at else None,
                }
                users_data.append(user_info)

            return users_data
        except Exception as e:
            # Handle other exceptions
            raise Exception(f'An error occurred: {str(e)}')

    # Method for adding new user
    @staticmethod
    def add_user(data):
        try:
            # Check if the user already exists
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user:
                return jsonify({'error': 'User already exists'}), 400

            # Hash the password
            hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

            # Create a new user instance
            new_user = User(
                role=data['role'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                identifier=data['identifier'],
                address=data['address'],
                email=data['email'],
                phone=data['phone'],
                password=hashed_password,
                status=data['status'],
                gender=data['gender']
            )

            # Add the new user to the database
            db.session.add(new_user)
            db.session.commit()

            # Send welcome email to the user
            # send_welcome_email(new_user.email, data['password'])

            return jsonify({'message': 'User added successfully', 'id': new_user.id}), 201
        except Exception as e:
            # Handle other exceptions
            db.session.rollback()
            return jsonify({'error': f'An error occurred: {str(e)}'}), 500

    # Method for getting user details by id service
    @staticmethod
    def get_user_by_id(user_id):
        try:
            # Check if the user exists
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404

            user_data = {
                'id': user.id,
                'identifier': user.identifier,
                'role': user.role,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone': user.phone,
                'email': user.email,
                'address': user.address,
                'status': user.status,
                'created_at': user.created_at,
                'updated_at': user.updated_at,
                'gender': user.gender,
                'images': [image.url for image in user.images]
            }

            return jsonify({'user': user_data}), 200

        except Exception as ex:
            return jsonify({'error': f'An error occurred: {str(ex)}'}), 500

    @staticmethod
    def delete_user(user_id):
        try:
            # Check if the user exists
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            # Query attendance records related to the user
            attendance_records = Attendance.query.filter_by(user_id=user_id).all()

            # Delete related attendance records
            for attendance_record in attendance_records:
                db.session.delete(attendance_record)

            # Query qrcode records related to the user
            qrCode_records = QRCode.query.filter_by(user_id=user_id).all()

            # Delete related qrcode records
            for qrcode_recode in qrCode_records:
                db.session.delete(qrcode_recode)

            db.session.commit()

            # Perform the deletion
            db.session.delete(user)
            db.session.commit()

            return jsonify({'message': 'User deleted successfully'}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'An error occurred: {str(e)}'}), 500

    @staticmethod
    def get_users_with_options(page, per_page, sort_by, order, custom_filter):
        try:
            # Query the database based on the provided options
            query = User.query

            # Apply filtering if custom_filter is provided
            if custom_filter:
                # Split the custom_filter into individual conditions (e.g., role=admin, status=active)
                conditions = [condition.strip() for condition in custom_filter.split(',')]

                # Build a list of filter expressions using OR conditions
                or_conditions = []
                for condition in conditions:
                    field, value = condition.split('=')
                    or_conditions.append(getattr(User, field) == value)

                # Apply OR conditions
                query = query.filter(or_(*or_conditions))

            # Apply sorting
            if order == 'asc':
                query = query.order_by(getattr(User, sort_by).asc())
            else:
                query = query.order_by(getattr(User, sort_by).desc())

            # Perform pagination
            users = query.paginate(page=page, per_page=per_page)

            return users

        except Exception as ex:
            return jsonify({'error': f'An error occurred: {str(ex)}'}), 500

    @staticmethod
    def suggest_users(name_query, max_results=10, relevance_threshold=60):
        try:
            # Query users whose first or last name partially matches the provided query
            matching_users = User.query.filter(
                (User.first_name.ilike(f'%{name_query}%')) | (User.last_name.ilike(f'%{name_query}%'))
            ).all()

            # Create a list of choices with usernames
            choices = [f'{user.first_name} {user.last_name}' for user in matching_users]

            # Use process.extractBests to get all relevant suggestions
            results = process.extractBests(name_query, choices, limit=None)

            # Separate arrays for suggestion names and details
            suggestion_names = []
            suggestion_details = []

            # Loop through the matching users and results
            for user, result in zip(matching_users, results):
                if result[1] >= relevance_threshold:
                    # Add suggestion name to the list
                    suggestion_names.append(f'{user.first_name} {user.last_name}')

                    # Add suggestion details to the list
                    suggestion_details.append({
                        'id': user.id,
                        'identifier': user.identifier,
                        'role': user.role,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'address': user.address,
                        'email': user.email,
                        'phone': user.phone,
                        'gender': user.gender,
                        'status': user.status,
                        'created_at': user.created_at,
                        'updated_at': user.updated_at if user.updated_at else None,
                    })

            # Limit the suggestions to max_results
            suggestion_names = suggestion_names[:max_results]
            suggestion_details = suggestion_details[:max_results]

            # Combine the arrays into a third array
            suggested_users_combined = {
                'suggestions': suggestion_names,
                'results': suggestion_details
            }

            return suggested_users_combined

        except Exception as ex:
            return jsonify({'error': f'An error occurred: {str(ex)}'}), 500



