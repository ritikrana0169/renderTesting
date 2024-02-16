from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.routes.user_routes import role_required
from app.services.admin_overview_service import AdminOverviewService

overview_blueprint = Blueprint('overview', __name__)

@overview_blueprint.route('/admin/overview', methods=['GET'])
# @jwt_required()
# @role_required('Admin')
def get_admin_overview():
    response = AdminOverviewService.get_admin_overview()
    return response
