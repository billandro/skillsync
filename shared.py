from firebase_admin import db, auth
import click, string, random, json, os

def read_from_database(path):
    ref = db.reference(path)
    return ref.get()


def add_meeting_to_database(the_data:object, meeting_id:str):
    ref = db.reference(f"/Meetings/{meeting_id}")
    ref.set(the_data)


def add_workshop_requests_to_database(the_data:object, workshop_id:str):
    ref = db.reference(f"/Workshop Requests/{workshop_id}")
    ref.set(the_data)


def validate_not_empty(ctx, param, value):
    if not value:
        raise click.BadParameter("Input cannot be empty")
    return value


def list_mentors(mentors:list, current_user_id):
    """Ensures that there are mentors to begin with. If not an error message is displayed."""
    available_mentors = False
    try:
        for i in range(len(mentors)):
            mentor_id, mentor_data = mentors[i]

            if i == 0 and mentor_id != current_user_id:
                click.secho("Available mentors:", fg="blue")

            if mentor_data.get("role") == "mentor" and mentor_id != current_user_id:
                click.echo(f"\nMentor {i + 1}:")
                click.echo(f'Name: {mentor_data.get("full_name") or mentor_data.get("first_name")}')
                click.echo(f'Email: {mentor_data.get("email")}')
                click.echo(f'Expertise: {mentor_data.get("expertise")}')
                available_mentors = True
        
        if not available_mentors:
            click.secho(f"Unfortunately, there are no mentors available...", fg="red", bg="white", blink=True)
            return available_mentors
        return available_mentors

    except Exception as e:
        click.secho(f"{e}: Unfortunately, there are no mentors available...", fg="black", bg="white", blink=True)
        return available_mentors


def list_workshops():
    data = read_from_database("/Workshop Requests")
    i = 0

    try:
        # If user is indeed signed in. List all upcoming workshops
        for k,v in data.items():
            if i == 0:
                click.secho(f"\nUpcoming workshops:\n", fg="blue")

            click.echo(f"Topic {i + 1} - {v['topic']}")
            i += 1
    except Exception as e:
        click.secho(f"\nUnfortunately, there are no upcoming workshops...", fg="red", bg="white", blink=True)


def request_workshop(topic:str, id:str, date_requested:str):
    """This function will create a workshop request instance.

    It will also generate a unique random workshop id.
    """
    the_data = {
        "requestor_id": id,
        "topic": topic,
        "date_requested": date_requested
    }

    characters = string.ascii_letters + string.digits
    workshop_id = "".join(random.choice(characters) for _ in range(28))

    add_workshop_requests_to_database(the_data, workshop_id)


def view_user_confirmed_bookings(user_uid):
    """This function first checks if there are any meetings in the database.
    If there are, it will check if the user has any. If not, it will
    alert the user.
    """
    meetings_data = read_from_database("/Meetings")
    i = 0

    try:
        confirmed_booking = False
        # Checks for confirmed meetings. For mentoring, being mentored, 
        # and peer sessions.
        for meeting_id, value in meetings_data.items():
            if value["mentor_id"] == user_uid and value["status"] == "confirmed":
                if i == 0:
                    click.echo("Your confirmed bookings:")

                click.echo(f"\nBooking {i + 1}:")
                user = auth.get_user(value["mentee_id"])
                click.echo(f"Mentoring session with {user.get('full_name') or user.get('first_name')}")
                confirmed_booking = True
                i += 1
                continue

            if  value["mentee_id"] == user_uid and value["status"] == "confirmed":
                if i == 0:
                    click.echo("Your confirmed bookings:")

                click.echo(f"\nBooking {i + 1}:")
                user = auth.get_user(value["mentor_id"])
                click.echo(f"Mentor session with {user.get('full_name') or user.get('first_name')}")
                confirmed_booking = True
                i += 1
                continue

            if  value["peer_id"] == user_uid and value["status"] == "confirmed":
                if i == 0:
                    click.echo("Your confirmed bookings:")

                click.echo(f"\nBooking {i + 1}:")
                user = auth.get_user(value["mentor_id"])
                click.echo(f"Peer session with {user.get('full_name') or user.get('first_name')}")
                confirmed_booking = True
                i += 1
                continue

        if not confirmed_booking:
            click.secho("You have no confirmed bookings.", fg="magenta", underline=True)

    except Exception as e:
        click.secho(f"You have no scheduled meetings in the system.", fg="red", underline=True)


def save_session(data, file):
    """Save session details to a file"""
    with open(file, "w") as f:
        json.dump(data, f)


def load_session(file):
    """Load session details from a file"""
    if os.path.exists(file):
        if os.path.getsize(file) == 0:
            return {"session": None, "id_token": None, "uid": None}
        else:
            with open(file, "r") as f:
                return json.load(f)
            

def list_peers(peers:list, current_user):
    """Ensures that there are peers to begin with. If not an error message is displayed."""
    available_peers = False
    try:
        for i in range(len(peers)):
            peer_id, peer_data = peers[i]

            if not available_peers and peer_id != current_user:
                click.secho("Available peers:", fg="blue")

            if peer_data["role"] == "peer" and peer_id != current_user:
                click.echo(f"\nPeer {i + 1}:")
                click.echo(f'Name: {peer_data["first_name"]}')
                click.echo(f'Email: {peer_data["email"]}')
                click.echo(f'Expertise: {peer_data["expertise"]}')
                available_peers = True
        
        if not available_peers:
            click.secho(f"Unfortunately, there are no peers available...", fg="red", bg="white", blink=True)
            return available_peers

        return available_peers

    except ValueError as e:
        click.secho(f"{e}: Peers list is empty.", fg="black", bg="white", blink=True)
        return available_peers


def checkInvaliSession(ctx):
    the_session = load_session("session.json")
    try:
        valid = auth.verify_id_token(id_token=the_session["id_token"])
        # click.secho(f"Valid: {json.load(valid)}")
        return the_session["session"], the_session["id_token"], the_session["uid"]
    except Exception as e:
        # click.secho(f"You need to Sign in", fg="red")
        save_session({"session": None, "uid": None, "id_token": None}, "session.json")
        ctx.obj["session"] = None
        ctx.obj["uid"] = None
        ctx.obj["id_token"] = None
        return ctx.obj["session"], ctx.obj["id_token"], ctx.obj["uid"]


def list_meetings(user_id:str):
    meetings = read_from_database("/Meetings")
    
    scheduled_meetings = False
    try:
        for i in range(len(meetings)):
            meeting_id, meeting_data = meetings[i]
            
            if i == 0:
                click.secho("Your scheduled meetings:", fg="blue")

            if meeting_data.get("peer_id") == user_id or meeting_data.get("mentor_id") == user_id:
                click.echo(f"\nMeeting {i + 1}:")
                click.echo(f'Time: {meeting_data.get("time")}')
                scheduled_meetings = True

        if not meetings:
            click.secho("There are no meetings in the system.", fg="red")
            return scheduled_meetings

        return scheduled_meetings
            
    except Exception as e:
        click.secho(f"You have no scheduled meetings: {e}.")
        return scheduled_meetings
        

def find_the_peer_or_mentor(user_id:str):
    users = read_from_database("/Users")

    user_available = False
    try:
        for i in range(len(users)):
            users_uid, user_data = users[i]

            if users_uid == user_id:
                user_available = True
                return users_uid
            
        if not user_available:
            click.secho("The user who you booked a meeting with was not found.", fg="red")
            return

    except Exception as e:
        click.secho(f"No users available in the database. {e}", fg="red")
