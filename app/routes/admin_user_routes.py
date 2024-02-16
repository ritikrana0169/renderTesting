# admin_user_route.py
import re
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.routes.admin_user_update_route import is_valid_email, is_valid_password, is_valid_phone
from app.routes.user_routes import role_required
from app.services.admin_user_service import AdminUserService
from flask import request

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/welcome')
# @jwt_required()
def greet():
    return jsonify({'message': 'Hello world'})


@user_blueprint.route('/admin/users/<int:page>/<int:per_page>/<string:sort_by>/<string:order>/',
                      methods=['GET'])
@user_blueprint.route('/admin/users/<int:page>/<int:per_page>/<string:sort_by>/<string:order>/<string:filter>',
                      methods=['GET'])
# @jwt_required()
# @role_required('Admin')
def get_users_with_options(page, per_page, sort_by, order, filter=None):
    """
    Method:GET, endpoint: /api/admin/users/2/5/address/desc/role=user
    in this request:
     /api/admin/users/page=2/per_page_data=5/sort_by=address/order_by=desc/filter=> role=user
     in filter part one can also send: status=active, role=admin
     note: filter is optional
    """
    try:
        # Call the service method to get users with options
        users = AdminUserService.get_users_with_options(
            page=page, per_page=per_page, sort_by=sort_by, order=order, custom_filter=filter
        )

        if not users.items:
            return jsonify({'message': 'No users found with the specified criteria'}), 200

        # Convert the users to a JSON response
        users_data = [{
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
        } for user in users.items]

        # Create a pagination response
        pagination_data = {
            'total_items': users.total,
            'total_pages': users.pages,
            'current_page': users.page,
            'next_page': users.next_num if users.has_next else None,
            'prev_page': users.prev_num if users.has_prev else None,
            'per_page': users.per_page,
        }

        return jsonify({'users': users_data, 'pagination': pagination_data}), 200
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


@user_blueprint.route('/admin/users', methods=['GET'])
# @jwt_required()
# @role_required('Admin')
def get_all_users():
    try:
        # Get pagination parameters from the request
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        # Call the service method to get paginated users
        users_data = AdminUserService.get_paginated_users(page=page, per_page=per_page)

        if not users_data:
            return jsonify({'message': 'No users found in the database'}), 200

        return jsonify(users_data), 200
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


@user_blueprint.route('/admin/users', methods=['POST'])
# @jwt_required()
# @role_required('Admin')
def add_user():
    """ POST request data
        {
            "identifier": "asd123",
            "role": "User",
            "first_name": "Ankit",
            "last_name": "Kumar",
            "email": "ankit@gmail.com",
            "password": "ankit@123",
            "address": "Delhi",
            "phone": "1234567890",
            "status": "Active",
            "gender": "Male"
        }
    """

    # Get data from the request
    data = request.get_json()

    # Validate the request data
    if 'role' not in data or data['role'] not in ['User', 'Admin', 'Guest']:
        return jsonify({'error': 'Invalid role'}), 400

    if 'email' not in data or not is_valid_email(data['email']):
        return jsonify({'error': 'Invalid email format'}), 400

    if 'password' not in data or not is_valid_password(data['password']):
        return jsonify({'error': 'Invalid password format'}), 400

    if 'phone' not in data or not is_valid_phone(data['phone']):
        return jsonify({'error': 'Invalid phone number format'}), 400

    if 'status' not in data or data['status'] not in ['Active', 'Inactive']:
        return jsonify({'error': 'Invalid status'}), 400

    # Validate the gender field
    if 'gender' not in data or data['gender'] not in ['Male', 'Female', 'Other']:
        return jsonify({'error': 'Invalid gender'}), 400

    response = AdminUserService.add_user(data)
    return response


# Get the user by id

@user_blueprint.route('/admin/users/<int:user_id>', methods=['GET'])
# @jwt_required()
# @role_required('Admin')
def get_user(user_id):
    # Validate for user_id
    if not isinstance(user_id, int) or user_id <= 0:
        return jsonify({'error': 'Invalid user ID'}), 400

    response = AdminUserService.get_user_by_id(user_id)
    return response


# Delete the user by id
@user_blueprint.route('/admin/users/<int:user_id>', methods=['DELETE'])
# @jwt_required()
# @role_required('Admin')
def delete_user(user_id):
    # Validate user_id
    if user_id <= 0:
        return jsonify({'error': 'Invalid user_id'}), 400

    response = AdminUserService.delete_user(user_id)
    return response


@user_blueprint.route('/admin/users/suggest', methods=['GET'])
# @jwt_required()
# @role_required('Admin')
def suggest_usernames():
    """
    Method: GET, endpoint: /admin/users/suggest
    Example request: /api/admin/users/suggest?name=john
    Example response:
    {
        "results": [
            {
                "address": "123 Main St",
                "created_at": "2023-12-24T23:33:16",
                "email": "john.doe@example.com",
                "first_name": "John",
                "gender": "Male",
                "id": 1,
                "identifier": "1",
                "last_name": "Doe",
                "phone": "123-456-7890",
                "role": "Admin",
                "status": "Active",
                "updated_at": "2023-12-24T23:33:16"
            },
            {
                "address": "789 Pine St",
                "created_at": "2023-12-24T23:33:16",
                "email": "robert.johnson@example.com",
                "first_name": "Robert",
                "gender": "Male",
                "id": 3,
                "identifier": "3",
                "last_name": "Johnson",
                "phone": "555-123-4567",
                "role": "Admin",
                "status": "Active",
                "updated_at": "2023-12-24T23:33:16"
            }
        ],
        "suggestions": [
            "John Doe",
            "Robert Johnson"
        ]
    }
    """
    try:
        # Get the name parameter from the query string
        name_query = request.args.get('name')

        # Validate that the name_query is present
        if not name_query:
            return jsonify({'error': 'Name parameter is required'}), 400

        # Call the service method to get user suggestions
        suggested_users = AdminUserService.suggest_users(name_query)

        if not suggested_users:
            return jsonify({'message': 'No usernames found for the specified name'}), 200

        # Return the suggested users as JSON response
        return jsonify(suggested_users), 200

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

