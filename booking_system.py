import datetime, click

from calender1 import create_calendar_event
from firebase_admin import auth
from shared import read_from_database, add_meeting_to_database
from shared import list_mentors, list_peers, list_meetings


def get_mentors_and_peers():
    """Display available peers"""

    mentor_list = []
    peer_list = []
    users = read_from_database("/Users")

    for key, value in users.items():
        if value["role"] == "mentor":
            mentor_list.append([key, value])
        elif value["role"] == "peer":
            peer_list.append([key, value])

    return mentor_list, peer_list


def book_mentor(mentors, chosen_mentors, user, done):
    """This will allow the user the opportunity to book one or more mentor sessions
    
    Will also handle any errors if no mentors are available.
    """
    while not done:
        chosen_mentor = click.prompt("\nEnter the mentor you would like to book by name (e.g. 'Bill')").strip().lower()
        
        found = False
        try:
            for i in range(len(mentors)):
                mentor_id, mentor_data = mentors[i]

                if chosen_mentor == mentor_data["first_name"].lower():
                    found = True
                    chosen_mentors.append(mentor_id)

                    event_date = click.prompt("Enter a date for session e.g. '2016-02-18'").strip()
                    if not booking_date(event_date):
                        click.secho("Error: The date you chose is during the weekend. Booking failed!", fg="red", bg="white", bold=True)
                        return
                    
                    start_time = click.prompt("Enter session start time ['07:00-16:59']")
                    end_time = click.prompt("Enter session end time ['07:01-17:00']")
                    if not booking_time(start_time, end_time):
                        click.secho("Error: The time you chose is not during business hours (07:00-17:00). Booking failed!", fg="red", bg="white", bold=True)
                        return
                    
                    meeting_id = {
                        "mentor_id": mentor_id,
                        "mentee_id": user.uid,
                        "time": f"{start_time}-{end_time}",
                        "status": "confirmed"
                    }

                    summary = f"This will be a mentor session. The session is on {mentor_data['expertise']}."
                    the_id = create_calendar_event(user.email, mentor_data["email"], summary, event_date, start_time, end_time)
                    add_meeting_to_database(meeting_id, the_id)

            if not found:
                click.secho(f"\nChosen mentor, '{chosen_mentor}', is NOT in our system.", fg="red")

            select_again = click.confirm("\nWould you like to book another mentor?")
            if select_again:
                done = False
                continue
            else:
                click.secho("\nBooking completed successfully...", fg="green")
                done = True
                
        except Exception as e:
            click.secho(f"Unfortunately, there are no mentors available. {e}", fg="red", bg="white", blink=True)


def book_peer(peers, chosen_peers, user, done):
    """This will allow the user the opportunity to book one or more peer sessions
    
    Will also handle any errors if no peers are available.
    """
    while not done:
        chosen_peer = click.prompt("\nEnter the peer you would like to book by name (e.g. 'Bill')").strip().lower()
        
        found = False
        try:
            for i in range(len(peers)):
                peer_id, peer_data = peers[i]

                if chosen_peer == peer_data["first_name"].lower():
                    found = True
                    chosen_peers.append(peer_id)

                    event_date = click.prompt("Enter a date for session e.g. '2016-02-18'").strip()
                    if not booking_date(event_date):
                        click.secho("Error: The date you chose is during the weekend. Booking failed!", fg="red", bg="white", bold=True)
                        return
                    
                    start_time = click.prompt("Enter session start time ['07:00-16:59']")
                    end_time = click.prompt("Enter session end time ['07:01-17:00']")
                    if not booking_time(start_time, end_time):
                        click.secho("Error: The time you chose is not during business hours (07:00-17:00). Booking failed!", fg="red", bg="white", bold=True)
                        return
                    
                    meeting_id = {
                        "mentor_id": peer_id,
                        "peer_id": user.uid,
                        "time": f"{start_time}-{end_time}",
                        "status": "confirmed"
                    }
                    
                    summary = f"This will be a one-on-one peer session. The session is on {peer_data['expertise']}."
                    the_id = create_calendar_event(user.email, peer_data["email"], summary, event_date, start_time, end_time)
                    add_meeting_to_database(meeting_id, the_id)

            if not found:
                click.secho(f"\nChosen peer, '{chosen_peer}', is NOT in our system.", fg="red")

            select_again = click.confirm("\nWould you like to book another peer?")
            if select_again:
                done = False
                continue
            else:
                click.secho("\nBooking completed successfully...", fg="green")
                done = True
                
        except Exception as e:
            click.secho(f"Unfortunately, there are no peers available. {e}", fg="red", bg="white", blink=True)
            break


def booking_date(the_date):
    """Function to check if a date is a weekday"""
    event_date = datetime.datetime.strptime(the_date, "%Y-%m-%d")
    return event_date.weekday() < 5


def booking_time(start_time, end_time):
    """This function will check whether the requested time is during business hours"""
    business_start = datetime.datetime.strptime("07:00", "%H:%M")
    business_end = datetime.datetime.strptime("17:00", "%H:%M")

    start_time_dt = datetime.datetime.strptime(start_time, "%H:%M")
    end_time_dt = datetime.datetime.strptime(end_time, "%H:%M")

    return business_start <= start_time_dt < business_end and business_start < end_time_dt <= business_end
        

def request_meeting(email):
    """Book mentor/peers for session"""

    mentors, peers = get_mentors_and_peers()
    done = False
    chosen_mentors = []
    chosen_peers = []
    user = auth.get_user_by_email(email)

    booking = click.prompt("Would you like to book a mentor or peer session?", type=click.Choice(["peer", "mentor"], case_sensitive=True)).strip()

    if booking == "mentor":
        successful = list_mentors(mentors, user.uid)
        if successful:
            book_mentor(mentors, chosen_mentors, user, done)
    else:
        successful = list_peers(peers, user.uid)
        if successful:
            book_peer(peers, chosen_peers, user, done)


def cancel_meeting(user_id):
    scheduled_meetings = list_meetings(user_id)

    if scheduled_meetings:
        try:
            meetings = read_from_database("/Meetings")
        except Exception as e:
            click.secho(f"Error reading meetings from database: {str(e)}", fg="red")
            return
        
        cancelled_booking = click.prompt("Which scheduled meeting would you like to cancel? Enter the name of the individual (e.g. 'Bill')").strip().capitalize()

        user_exists = False
        for key, value in meetings.items():
            if cancelled_booking == value.get("first_name"):
                user_exists = True
                delete_meeting_ref = meetings.child(key)
                delete_meeting_ref.delete()
                click.secho(f"Booking with {cancelled_booking} was successfully removed.", fg="green")
                break

        if not user_exists:
            click.secho(
                "Booking cancellation failed. Try again with the correct name or ensure the meeting exists.",
                fg="yellow"
            )
        else:
            click.secho("No scheduled meetings found for this user.", fg="blue")
