from flask import jsonify
from app.models.model import User, Organization, Attendance
from sqlalchemy import select
from app.exception.admin_externalUser_exception import OrganizationException

class Allevent_attedance_history_service:
    def allevent_attedance_history():
        users = Organization.query.first().users
        if(users == None):
            raise OrganizationException('Organization not found.')
        p=0
        a=0
        for user in users:
            atd = Attendance.query.get(user_id=user.id,status='Present').count
            if(atd==0):
                p+=1
            else:
                a+=1
        data={'Absent':a,'Present':p}
        return data