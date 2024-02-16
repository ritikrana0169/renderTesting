from flask import Flask,Blueprint, jsonify, request
# from json import JSONEncoder
from flask_jwt_extended import jwt_required
from app.routes.user_routes import role_required
from urllib.parse import quote
from app.models.model import db
from app.services.admin_eventUser_service import admin_eventUser_service 


eventUser_routes = Blueprint('eventUser_routes', __name__)


# Add user in the event with the help of event id and user id
@eventUser_routes.route('/admin/events/<int:event_Id>/add_user/<int:user_Id>', methods=['POST'])
# @jwt_required()
# @role_required('Admin')
def add_user_inEvent(event_Id,user_Id):
    resCODE = 200 
    event = admin_eventUser_service.add_User_in_event(event_Id,user_Id)
    if(event["message"] == "User add successfully"):
        resCODE = 200
    else:
        resCODE = 404
    # print(resCODE)
    return jsonify(event),resCODE


 # Get all users of a specific event with the help of event id 
@eventUser_routes.route('/admin/events/<int:event_Id>/user', methods=['GET'])
# @jwt_required()
# @role_required('Admin')
def getAllUser_ofEvent(event_Id):
    resCODE = 200 
    allUsers_ofE = admin_eventUser_service.getAll_user_ofEvent(event_Id)
    if(allUsers_ofE["message"] == "event not found" or allUsers_ofE["message"] == "No any User in this event"):
        resCODE = 404
    else:
        resCODE = 200
    # print(resCODE)
    return jsonify(allUsers_ofE),resCODE


# Delete user from the event with the help of event id and user id
@eventUser_routes.route('/admin/events/<int:event_Id>/user/<int:user_Id>', methods=['DELETE'])
# @jwt_required()
# @role_required('Admin')
def deleteUser_fromEvent(event_Id,user_Id):
    resCODE = 200 
    response = admin_eventUser_service.delete_User_from_Event(event_Id,user_Id)
    if(response["message"] == "event not found" or response["message"] == "User not found" or response["message"] == "User is not in event"):
        resCODE = 404
    else:
        resCODE = 200
    # print(resCODE)
    return jsonify(response),resCODE


# Add many Users in the event with the help of event id and array of users id
@eventUser_routes.route('/admin/events/<int:event_Id>/add_many_users', methods=['POST'])
# @jwt_required()
# @role_required('Admin')
def add_many_users_inEvent(event_Id):

    data = request.get_json()
    resCODE = 200 
    response = admin_eventUser_service.add_many_Users_in_event(event_Id,data)
    if(response["message"] == "event not found" or response["message"] == "Provide one or many user id" or response["message"] == "0 User added"):
        resCODE = 404
    else:
        resCODE = 200
    # print(resCODE)
    return jsonify(response),resCODE

# Delete many Users in the event with the help of event id and array of users id
@eventUser_routes.route('/admin/events/<int:event_Id>/delete_many_users', methods=['DELETE'])
# @jwt_required()
# @role_required('Admin')
def delete_many_users_inEvent(event_Id):

    data = request.get_json()
    resCODE = 200 
    response = admin_eventUser_service.delete_many_Users_in_event(event_Id,data)
    if(response["message"] == "event not found" or response["message"] == "Provide one or many user id" or response["message"] == "0 User deleted"):
        resCODE = 404
    else:
        resCODE = 200
    # print(resCODE)
    return jsonify(response),resCODE


# See user activity by user identifier
@eventUser_routes.route('/admin/user/activity/<string:user_identifier>', methods=['GET'])
# @jwt_required()
# @role_required('Admin')
def get_user_activity(user_identifier):
    result, status_code = admin_eventUser_service.get_user_activity(user_identifier)
    return jsonify(result), status_code


# Search event by event title
@eventUser_routes.route('/admin/events/search', methods=['GET'])
# @jwt_required()
# @role_required('Admin')
def search_event_by_title():
    title = request.args.get('title')
    result, status_code = admin_eventUser_service.search_event_by_title(title)
    return jsonify(result), status_code