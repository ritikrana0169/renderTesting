from flask import Blueprint, jsonify
from app.services.admin_overview_service import AdminOverviewService

overview_blueprint = Blueprint('overview', __name__)

@overview_blueprint.route('/admin/overview', methods=['GET'])
def get_admin_overview():
    response = AdminOverviewService.get_admin_overview()
    return response
