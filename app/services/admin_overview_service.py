from flask import jsonify
from app.models.model import User, Device, Event

class AdminOverviewService:
    @staticmethod
    def get_admin_overview():
        try:
            # Get counts from the database
            total_users = User.query.filter_by(role='User').count()
            total_guests = User.query.filter_by(role='Guest').count()
            total_admins = User.query.filter_by(role='Admin').count()
            total_events = Event.query.count()
            total_devices = Device.query.count()

            # Return the overview data
            overview_data = {
                'total_users': total_users,
                'total_guests': total_guests,
                'total_admins': total_admins,
                'total_events': total_events,
                'total_devices': total_devices
            }

            return jsonify(overview_data), 200
        except Exception as e:
            return jsonify({'error': f'An error occurred: {str(e)}'}), 500
