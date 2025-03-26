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
        ctx.obj["session"] = ctx.obj["id_token"]
    else:
        ctx.obj["id_token"], ctx.obj["uid"] = sign_up()
        ctx.obj["session"] = ctx.obj["id_token"]

    create_session(ctx)
    save_session(ctx.obj, "session.json")
    click.secho("Session saved successfully!", fg="green")


@main.command(name="View Workshops")
@click.pass_context
def view_workshops(ctx):
    """Lists upcoming workshops and mentors available for booking.
    
    This function requires user authentication and session creation.
    Local imports are used to break circular dependency.
    """
    from booking_system import get_mentors_and_peers
    from shared import list_workshops, list_mentors, checkInvaliSession

    session, id_token, uid = checkInvaliSession(ctx)

    if session and id_token:
        # Get 2D list for both mentors and peers
        mentors, peers = get_mentors_and_peers()

        # List all available mentors and upcoming workshops from firebase
        list_mentors(mentors, uid)
        list_workshops()
    else:
        click.secho("You must sign in to view workshops and mentors...", fg="yellow", blink=True)


@main.command(name="Request Meeting")
@click.pass_context
def request_session(ctx):
    """Requests a meeting with a mentor.
    
    This function requires user authentication and session creation.
    """
    from booking_system import request_meeting
    from shared import checkInvaliSession

    session, id_token, uid = checkInvaliSession(ctx)
    if session and uid:
        user = auth.get_user(uid=uid)
        request_meeting(user.email)
    else:
        click.secho("You must sign in to request a session...", fg="yellow", blink=True)


@main.command(name="View Bookings")
@click.pass_context
def view_bookings(ctx):
    """Displays a list of confirmed bookings.

    This function requires user authentication and session creation.
    """
    from shared import view_user_confirmed_bookings, checkInvaliSession

    
    session, id_token, uid = checkInvaliSession(ctx)

    if session and id_token:
        view_user_confirmed_bookings(uid)
    else:
        click.secho("You must sign in to view your confirmed bookings...", fg="yellow", blink=True)


@main.command(name="Request Workshop")
@click.pass_context
def request_a_workshop(ctx):
    """ Request a workshop from users

    This function requires user authentication and session creation.
    """
    from shared import request_workshop, checkInvaliSession 

    session, id_token, uid = checkInvaliSession(ctx)

    if session and id_token:
        topic = click.prompt("What topic would you like covered in this workshop?", type=str)
        date_requested = click.prompt("Enter a date for the workshop. Format 'year-month-day'", type=str)
        
        request_workshop(topic, uid, date_requested)
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