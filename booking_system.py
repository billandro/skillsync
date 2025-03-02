import datetime, click

from calender1 import create_calender_event
from firebase_admin import auth, db
from firebase_admin import credentials
from main import connect_to_database
from shared import read_from_database, add_to_database, validate_not_empty


@click.group()
def cli_2():
    """This is the grouper of all the commands"""
    pass


def get_peers_and_peers():
    """Display available peers"""
    connect_to_database()

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
    """This will allow the user the opportunity to book one or more mentor sessions"""
    summary = f"This will be a mentor session. The session is on {user.expertise}."

    while not done:
        chosen_mentor = click.option(prompt="Enter the mentor you would like to book by name (e.g. 'Bill')", value_proc=validate_not_empty).strip().lower()
        
        for i in range(len(mentors)):
            for key, value in mentors[i][1].items():
                if chosen_mentor == value["first_name"]:
                    chosen_mentors.append(key)

                    event_date = click.prompt("Enter a date for session e.g. 2016-02-18").strip()
                    if not booking_date(event_date):
                        click.secho("Error: The date you chose in during the weekend!", fg="red")
                        return
                    
                    start_time = click.prompt("Enter session start time ['07:00-16:59']")
                    end_time = click.prompt("Enter session endtime ['07:01-17:00']")
                    if not booking_time(start_time, end_time):
                        click.secho("Error: The time you chose is not during business hours (07:00-17:00)!", fg="red")
                        return
                    
                    meeting_id = {"mentor_id": key, "mentee_id": user.uid, "time": f"{start_time}-{end_time}", "status": "active"}
                    add_to_database(meeting_id, key)
                    create_calender_event(user.email, value["email"], summary, event_date, start_time, end_time)
                    return

        click.secho(f"Chosen mentor, '{chosen_mentor}', is not in our system.", fg="red")

        select_again = click.confirm("Would you like to book another mentor?")
        if select_again == "y":
            done = False
            continue
        else:
            click.echo("Booking completed successfully...")
            done = True


def booking_date(the_date):
    """Function to check if a date is a weekday"""
    event_date = datetime.datetime.strptime(the_date, "%Y-%m-%d")
    return event_date.weekday() < 5


def booking_time(start_time, end_time):
    """Function to check if time is during business hours"""
    business_start = datetime.datetime.strptime("07:00", "%H:%M")
    business_end = datetime.datetime.strptime("17:00", "%H:%M")

    return business_start <= start_time < business_end and business_start < end_time <= business_end
        

@cli_2.command()
def request_meeting(email):
    """Book mentor/peers for session"""

    mentors, peers = get_peers_and_peers()
    done = False
    chosen_mentors = []
    chosen_peers = []
    user = auth.get_user_by_email(email)

    booking = click.prompt("Would you like to book a mentor or peer session? ['peer'/'mentor']", type=click.Choice(["peer", "mentor"], case_sensitive=False))

    if booking == "mentor":
        book_mentor(mentors, chosen_mentors, user, done)
    else:
        pass


if __name__ == "__main__":
    cli_2()