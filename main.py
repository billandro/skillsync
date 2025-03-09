import click
from authentication import login, sign_up
from database import connect_to_database
from firebase_admin import auth
from shared import save_session, load_session


@click.group()
@click.pass_context
def main(ctx):
    """Main entry point for the CLI"""
    connect_to_database()
    ctx.obj = load_session("session.file") or {}


def create_session(ctx):
    """Create session cookie and id token for authenticated user"""
    if not ctx.obj.get("id_token"):
        click.secho("Error: No ID token found. Cannot create session.", fg="red", blink=True)
        return

    try:
        auth.verify_id_token(ctx.obj["id_token"])
        ctx.obj["session"] = auth.create_session_cookie(id_token=ctx.obj["id_token"], expires_in=3600)
        save_session(ctx.obj, "session.json")
        click.secho("Session created successfully!", fg="green")
    except auth.InvalidIdTokenError:
        click.secho("The provided ID token is invalid.", fg="red", blink=True)
    except Exception as e:
        click.secho(f"Unexpected error occurred while creating session: {e}", fg="red", blink=True)


@main.command(name="Login")
@click.pass_context
def authenticate(ctx):
    """Handles user authentication based on returning status."""
    returning_user = click.prompt("Are you a returning user?", type=click.Choice(["y", "n"], case_sensitive=True))
    
    if returning_user == "y":
        ctx.obj["id_token"], ctx.obj["uid"] = login()
    else:
        ctx.obj["id_token"] = sign_up()

    create_session(ctx)
    save_session(ctx.obj, "session.json")
    click.secho("Session saved successfully!", fg="green")


@main.command(name="View Workshops")
def view_workshops():
    """Lists upcoming workshops and mentors available for booking.
    
    This function requires user authentication and session creation.
    Local imports are used to break circular dependency.
    """
    from booking_system import get_mentors_and_peers
    from shared import list_workshops, list_mentors

    data = load_session("session.json")
    if data["session"]:
        # Get 2D list for both mentors and peers
        mentors, peers = get_mentors_and_peers()

        # List all available mentors and upcoming workshops from firebase
        list_mentors(mentors, data["uid"])
        list_workshops()
    else:
        click.secho("You must sign in to view workshops and mentors...", fg="yellow", blink=True)


@main.command(name="Request Meeting")
def request_session():
    """Requests a meeting with a mentor.
    
    This function requires user authentication and session creation.
    """
    from booking_system import request_meeting
    global session, user_uid
    
    create_session()
    if session is not None and user_uid is not None:
        user = auth.get_user(uid=user_uid)
        request_meeting(user.email)
    else:
        click.secho("Please sign in to request a session...", fg="yellow", blink=True)


@main.command(name="View Bookings")
def view_bookings():
    """Displays a list of confirmed bookings.

    This function requires user authentication and session creation.
    """
    from shared import view_user_confirmed_bookings
    global session, user_uid

    create_session()
    if session is not None and user_uid is not None:
        view_user_confirmed_bookings(user_uid)
    else:
        click.secho("Please sign in to view your bookings...", fg="yellow", blink=True)


@main.command(name="Request Workshop")
def request_a_workshop():
    """ Request a workshop from users

    This function requires user authentication and session creation.
    """
    from shared import request_workshop
    global session, user_uid

    create_session()
    if session is not None and user_uid is not None:
        topic = click.prompt("What topic would you like covered in this workshop?", type=str)
        date_requested = click.prompt("Enter a date for the workshop. Format 'year-month-day'", type=str)
        
        request_workshop(topic, user_uid, date_requested)
    else:
        click.secho("Please sign in to request a workshop...", fg="yellow", blink=True)


@main.command(name="Sign Out")
@click.pass_context
def end_session(ctx):
    """Ends the session cookie or signs out the authenticated user"""
    ctx.obj = load_session("session.json")

    if not ctx.obj.get("session"):
        click.secho("You can't sign out if you were never signed in, silly.", fg="magenta")
        return

    try:
        decoded_token = auth.verify_session_cookie(ctx.obj["session"])
        user = auth.get_user(decoded_token["uid"])
        ctx.obj = {"session": None, "id_token": None}  # Clear session
        click.secho(f"Signed out {user.display_name or user.email}. Goodbye!", fg="magenta")
    except auth.InvalidSessionCookieError:
        click.secho("Session is already invalid or expired.", fg="red")
    save_session(ctx.obj, "session.json")  # Persist cleared session


if __name__ == "__main__":
    main()