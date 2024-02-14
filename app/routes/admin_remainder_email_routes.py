# route.py
from flask import Flask, Blueprint, jsonify, request
from app.models.model import User, Event, db
from app.services.admi_remainder_email_sevice import send_email

remainder_email = Blueprint('remainder_email', __name__)


# API endpoint to send reminder emails
@remainder_email.route('/send-reminder-email', methods=['POST'])
def send_reminder_email():
    data = request.json
    user_id = data.get('user_id')
    event_id = data.get('event_id')

    # Fetch user and event details from the database
    user = User.query.get(user_id)
    event = Event.query.get(event_id)

    if user and event:
        # Construct recipient email
        if user not in event.participants:
            return {'error': f'Warning: User with identifier {user_id} is not assigned to the event with id {event_id}'}, 400
        
        receiver_email = user.email
        Subject=f'Reminder: Join Our Event {event.event_title}'
        # Construct email body
        body =  f'''Dear {user.first_name+" "+user.last_name},

I hope this email finds you well. We are thrilled to remind you about the upcoming offline event, {event.event_title}, taking place on {event.event_date} at {event.event_location}.

As one of our valued participants, your presence will greatly contribute to the success of the event. We have curated an engaging agenda that includes insightful discussions, networking opportunities, and valuable takeaways.

We kindly request your prompt attendance at the event. If you haven't already, please confirm your participation by replying to this email or by registering through the provided link.

Should you have any questions or require further information, please don't hesitate to reach out to us. We are here to assist you in any way we can.

Thank you for your attention, and we look forward to welcoming you to {event.event_title}.

Best regards,

[Masai school]
[Event Manager]
[MasaiSchool@masaischool.com]'''


        # Send email
        send_email(receiver_email, body,Subject)
        return jsonify({'message': 'Reminder email sent successfully.'}), 200
    else:
        return jsonify({'error': 'User or event not found.'}), 404


@remainder_email.route('/send-reminder-bulk-emails', methods=['POST'])
def send_reminder_emails():
    data = request.json
    event_id = data.get('event_id')
    users = data.get('users')  # List of user IDs

    event = Event.query.get(event_id)

    if event:
        for user_id in users:
            user = User.query.get(user_id)
            if user:
             if user  in event.participants:
            
                receiver_email = user.email
                Subject=f'Reminder: Join Our Event {event.event_title}'
                body = f'''Dear {user.first_name},

I hope this email finds you well. We are thrilled to remind you about the upcoming offline event, {event.event_title}, taking place on {event.event_date} at {event.event_location}.

As one of our valued participants, your presence will greatly contribute to the success of the event. We have curated an engaging agenda that includes insightful discussions, networking opportunities, and valuable takeaways.

We kindly request your prompt attendance at the event. If you haven't already, please confirm your participation by replying to this email or by registering through the provided link.

Should you have any questions or require further information, please don't hesitate to reach out to us. We are here to assist you in any way we can.

Thank you for your attention, and we look forward to welcoming you to {event.event_title}.

Best regards,

[Masai school]
[Event Manager]
[MasaiSchool@masaischool.com]'''




                send_email(receiver_email, body,Subject)
        
        return jsonify({'message': 'Reminder emails sent successfully.'}), 200
    else:
        return jsonify({'error': 'Event not found.'}), 404

