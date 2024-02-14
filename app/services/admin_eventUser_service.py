from sqlalchemy import text
from app.models.model import db,Event,User,Image,Attendance
from datetime import datetime, timedelta


class admin_eventUser_service:

    # Add user in the event with the help of event id and user id
    def add_User_in_event(event_Id,user_Id):

        string = ""
        event = Event.query.get(event_Id)
        if(event == None):
            string = "event not found"
        user = User.query.get(user_Id)
        if(user == None):
            string = "User not found"


        if(event and user):

            sql_query = text(f"""select * from user_events where user_id = {user_Id} and event_id = {event_Id};""")
            result = db.session.execute(sql_query)
            user_events = result.fetchall()

            if(user_events):
                # print("User allredy prsent in the event")
                return ({'Event_Title': event.event_title,"User":user.first_name+user.last_name,'Event_Type': event.event_type,"message":"User allredy prsent in the event"})
            else:
                # print("User add successfully")
                event.participants.append(user)
                db.session.commit()
                return ({'Event_Title': event.event_title,"User":user.first_name+user.last_name,'Event_Type': event.event_type,"message":"User add successfully"})
        else:
            return ({"message":string})
        
    
    # Get all users of a specific event with the help of event id 
    def getAll_user_ofEvent(event_Id):

        event = Event.query.get(event_Id)
        if(event):
            event_users = event.participants
            if(event_users):
                allUser_ofEvent = []
                for user in event_users:

                    pic = ""
                    user_image = Image.query.filter_by(user_id=user.id).first()
                    if(user_image == None):
                        pic = "User has no image"
                    else:
                        pic = user_image.url

                    userDictionary = {
                        'id':user.id,
                        'identifier': user.identifier,
                        'role': user.role,
                        'first_name': user.first_name,
                        "last_name":user.last_name,
                        "address":user.address,
                        "email":user.email,
                        "phone":user.phone,
                        "password":user.password,
                        "status":user.status,
                        "created_at":user.created_at,
                        "updated_at":user.updated_at,
                        "image":pic
                        # Add other fields as needed
                    }
                    allUser_ofEvent.append(userDictionary)
                    # print(pic)
                    # print(f"User ID: {user.id}, Name: {user.first_name} {user.last_name}")
                return ({"id":event.id,"event_title":event.event_title,"event_title":event.event_title,"event_description":event.event_description,"allUser":allUser_ofEvent,"message":"get all users"})
            else:
                return ({"id":event.id,"event_title":event.event_title,"event_title":event.event_title,"event_description":event.event_description,"message":"No any User in this event"})
        else:
            string = "event not found"
            return ({"message":string})
        

    # Delete user from the event with the help of event id and user id
    def delete_User_from_Event(event_Id,user_Id):
 
        string = ""
        event = Event.query.get(event_Id)
        if(event == None):
            string = "event not found"
        user = User.query.get(user_Id)
        if(user == None):
            string = "User not found"

        if(event and user):
            sql_query = text(f"""select * from user_events where user_id = {user_Id} and event_id = {event_Id};""")
            result = db.session.execute(sql_query)
            user_events = result.fetchall()
            # print(user_events)

            if(user_events):
                query = text(f"""delete from user_events where event_id = {event_Id} and user_id = {user_Id};""")
                result1 = db.session.execute(query)
                db.session.commit()
                
                return ({'Event_Title': event.event_title,"User":user.first_name+user.last_name,'Event_Type': event.event_type,"message":"User deleted successfully"})
            else:
                return ({'Event_Title': event.event_title,"User":user.first_name+user.last_name,'Event_Type': event.event_type,"message":"User is not in event"})
        else:
            return ({"message":string})
        

    # Add many Users in the event with the help of event id and array of users id
    def add_many_Users_in_event(event_Id,data):

        string = ""
        event = Event.query.get(event_Id)
        if(event == None):
            string = "event not found"
        
        if(len(data) == 0):
            string = "Provide one or many user id"


        if(event and len(data) > 0):
            status = []
            count = 0
            for i in data:
                if str(i).isdigit():
                    user = User.query.get(int(i))
                    if(user):
                        sql_query = text(f"""select * from user_events where user_id = {int(i)} and event_id = {event_Id};""")
                        result = db.session.execute(sql_query)
                        user_events = result.fetchall()
                        # print(user_events)

                        if(user_events):
                            status.append(f"User allredy prsent in the event with {i} id")
                        else:
                            status.append(f"User add successfully with {i} id")
                            count += 1
                            event.participants.append(user)
                            db.session.commit()

                    else:
                        status.append(f"user not found with {i} id")
                else:
                    status.append(f"{i} <= This is not digit provide digit")  
            # for j in status:
            #     print(j)
            return ({'Event_Title': event.event_title,"add status list":status,'Event_Type': event.event_type,"message": f"{count} User added"})
        else:
            return ({"message":string})
        
    
    #Delete many Users in the event with the help of event id and array of users id
    def delete_many_Users_in_event(event_Id,data):

        string = ""
        event = Event.query.get(event_Id)
        if(event == None):
            string = "event not found"
        
        if(len(data) == 0):
            string = "Provide one or many user id"


        if(event and len(data) > 0):
            status = []
            count = 0
            for i in data:
                if str(i).isdigit():
                    user = User.query.get(int(i))
                    if(user):
                        sql_query = text(f"""select * from user_events where user_id = {int(i)} and event_id = {event_Id};""")
                        result = db.session.execute(sql_query)
                        user_events = result.fetchall()
                        # print(user_events)

                        if(user_events):
                            count += 1
                            query = text(f"""delete from user_events where event_id = {event_Id} and user_id = {int(i)};""")
                            result1 = db.session.execute(query)
                            db.session.commit()
                            status.append(f"User deleted successfully with {i} id, {user.first_name} {user.last_name}")
                        else:
                            status.append(f"User is not in event with {i} id, {user.first_name} {user.last_name}")

                    else:
                        status.append(f"user not found with {i} id")
                else:
                    status.append(f"{i} <= This is not digit provide digit")  
            # for j in status:
            #     print(j)
            return ({'Event_Title': event.event_title,"delete status list":status,'Event_Type': event.event_type,"message": f"{count} User deleted"})
        else:
            return ({"message":string})
        
    
     # """
        # Get the activity details for a specific user, including event participation and attendance status.
        # - For each event the user participated in, checks attendance records on the event date.
        # - Classifies user's attendance status based on check-in and check-out times.
        # - Classifies user as present if check-in and check-out times fall within the event duration.
        # - Classifies user as late if check-in occurs after 15 minutes of event start time.
        # - Classifies user as absent if there's no attendance record or check-in/out times don't match event duration.
        # """
    def get_user_activity(user_identifier):
        try:
            # Get the user
            user = User.query.filter_by(identifier = user_identifier).first()
            print(user)

            if user:
                # Get the list of events for the user
                user_events = user.events

                # Initialize list to store user activity details
                user_activity = []

                prese = 0
                absen = 0

                for event in user_events:
                    # Check if there is attendance record for the user on the event date
                    attendance = Attendance.query.filter_by(user_id=user.id, date=event.event_date).first()

                    if attendance:
                        # Convert check-in time to datetime object
                        check_in_datetime = datetime.combine(event.event_date, attendance.check_in_time)

                        # Calculate the time difference from the event start and end time
                        time_difference_start = check_in_datetime - datetime.combine(event.event_date, event.start_time)
                        time_difference_end = check_in_datetime - datetime.combine(event.event_date, event.end_time)

                        # Check user's attendance status based on check-in and check-out times
                        if time_difference_start > timedelta(minutes=15):
                            # Check if user joined after the event end time
                            if time_difference_end > timedelta(minutes=0):
                                status = 'Absent'
                                absen += 1
                            else:
                                status = 'Late'
                        else:
                            status = 'Present'
                            prese += 1
                    else:
                        status = 'Absent'
                        absen += 1

                    # Prepare event details
                    event_details = {
                        'event_id': event.id,
                        'event_title': event.event_title,
                        'event_date': event.event_date.strftime('%Y-%m-%d'),
                        'start_time': event.start_time.strftime('%H:%M:%S'),
                        'end_time': event.end_time.strftime('%H:%M:%S'),
                        'status': status
                    }

                    # Prepare user activity details
                    user_activity.append({
                        'user_id': user.id,
                        'user_name': f'{user.first_name} {user.last_name}',
                        'event_details': event_details
                    })

                if not user_activity:
                    return {'messaage': 'Not found any activity for this user'}, 404

                # print(absen,prese)
                user_activity.append({
                    'Present':prese,
                    'Absent':absen
                })
                return user_activity, 200

            return {'error': 'User not found'}, 404

        except Exception as e:
            return {'error': str(e)}, 500


    # Search events by title 
    def search_event_by_title(title):

        if not title:
            return {'error': 'Title parameter is required'}, 400
        
        events = Event.query.filter(Event.event_title.ilike(f'%{title}%')).all()

        if not events:
            return {'message': 'No events found with the given title'}, 404

        # Serialize the events to JSON
        serialized_events = [{
            'event_id':event.id,
            'event_title': event.event_title,
            'event_type': event.event_type,
            'event_description': event.event_description,
            'event_location': event.event_location,
            'event_date': event.event_date.strftime('%Y-%m-%d'),
            'start_time': event.start_time.strftime('%H:%M:%S'),
            'end_time': event.end_time.strftime('%H:%M:%S'),
            'event_status': event.event_status,
            'created_at': event.created_at,
            'updated_at': event.updated_at,
            'repeat_type': event.repeat_type,
            'organization_id': event.organization_id
        } for event in events]
        return serialized_events,200