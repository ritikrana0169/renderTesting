from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import UniqueConstraint

# creating SQLAlchemy db
db = SQLAlchemy()

# user_events
user_events = db.Table('user_events',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                       db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
                       )


# event_devices
event_devices = db.Table('event_devices',
                         db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
                         db.Column('device_id', db.Integer, db.ForeignKey('device.id'))
                         )



# Organization class
class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    org_name = db.Column(db.String(255))
    org_type = db.Column(db.String(50))
    address = db.Column(db.String(255))
    contact_email = db.Column(db.String(255))
    contact_phone = db.Column(db.String(20))
    password = db.Column(db.String(255))
    active_path = db.Column(db.String(255))
    status = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.now())
    users = db.relationship('User', primaryjoin='User.organization_id == Organization.id', lazy=True, overlaps="users")
    events = db.relationship('Event', primaryjoin='Event.organization_id == Organization.id', lazy=True, overlaps="events")
    devices = db.relationship('Device', primaryjoin='Device.organization_id == Organization.id', lazy=True, overlaps="devices")
    attendances = db.relationship('Attendance', primaryjoin='Attendance.organization_id == Organization.id', lazy=True, overlaps="attendances")
    qr_code = db.relationship('QRCode', primaryjoin='QRCode.organization_id == Organization.id', lazy=True, overlaps="qr_code")


# User class
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(50), unique=True)
    role = db.Column(db.String(20))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    address = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    gender = db.Column(db.String(8))
    password = db.Column(db.String(255))
    status = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    images = db.relationship('Image', backref='user', lazy=True)
    events = db.relationship('Event', secondary='user_events', back_populates='participants')

    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    organization = db.relationship('Organization', foreign_keys=[organization_id], lazy=True, overlaps="users")

    # organization = db.relationship('Organization', backref='user', lazy=True)

    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()


# Image class
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    url = db.Column(db.String(255))


# Attendance class
class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    check_in_time = db.Column(db.Time)
    check_out_time = db.Column(db.Time)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=True)
    status = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    tags=db.Column(db.String(20),nullable=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    organization = db.relationship('Organization', foreign_keys=[organization_id], lazy=True, overlaps="attendances")

 
# Device class
class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    ip_address = db.Column(db.String(15))
    location = db.Column(db.String(255))
    passcode = db.Column(db.String(255))
    availability = db.Column(db.String(15))
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    organization = db.relationship('Organization', foreign_keys=[organization_id], lazy=True, overlaps="devices")


# Event code clas
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_title = db.Column(db.String(255))
    event_type = db.Column(db.String(20))
    event_description = db.Column(db.Text)
    event_location = db.Column(db.String(255))
    event_date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    event_status = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    repeat_type = db.Column(db.String(20))
    repeat_days = db.relationship('RepeatDay', secondary='repeat_days_events', back_populates='events')
    participants = db.relationship('User', secondary='user_events', back_populates='events')
    devices = db.relationship('Device', secondary='event_devices', backref='events')
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    organization = db.relationship('Organization', foreign_keys=[organization_id], lazy=True, overlaps="events")
    __table_args__ = (
        UniqueConstraint('event_title', 'event_date', 'event_location', 'start_time','event_type', name='unique_event_constraint'),
    )


# QR code class
class QRCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(350), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    imageUrl = db.Column(db.String(150))
    is_scanned = db.Column(db.Boolean, default=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    organization = db.relationship('Organization', foreign_keys=[organization_id], lazy=True, overlaps="qr_code")


# repeat_days_events table


repeat_days_events = db.Table(
    'repeat_days_events',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
    db.Column('repeat_day_id', db.Integer, db.ForeignKey('repeat_day.id')),
)


class RepeatDay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(20), unique=True)
    events = db.relationship('Event', secondary='repeat_days_events', back_populates='repeat_days')


class EmailError(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer,unique=True)
    event_id=db.Column(db.Integer)
