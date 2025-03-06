import click
from authentication import login, sign_up
from database import connect_to_database
from firebase_admin import auth

user_uid = None
session = None

@click.group()
def main():
    """Main entry point for the CLI"""
    connect_to_database()


@main.command(name="authenticate_user")
def authenticate():
    """Handles user authentication based on returning status."""
    global user_uid

    returning_user = click.prompt("Are you a returning user?", type=click.Choice(["y", "n"], case_sensitive=True))
    if returning_user == "y":
        user_uid = login()
    else:
        user_uid = sign_up()


def create_session():
    """Create session cookie and id token for authenticated user"""
    global session

    if session is None:
        try:
            token = auth.create_custom_token(uid=user_uid)
            try:
                session = auth.create_session_cookie(id_token=token, expires_in=3600)
            except Exception as e:
                click.secho(f"Unexpected error occurred while creating session cookie: {e}", fg="red", blink=True)
                return
        except ValueError:
            click.secho("Input parameter for creating a custom token was invalid.", fg="red", blink=True)
            return
        except auth.TokenSignError:
            click.secho("Unexpected error while signing a Firebase custom token.", fg="red", blink=True)
            return


@main.command(name="end_session")
def end_session():
    """Ends the session cookie or signs out the authenticated user"""
    global session, user_uid
    session = None
    user_uid = None


@main.command(name="view_workshops")
def view_workshops():
    """Lists upcoming workshops and mentors available for booking.
    
    This function requires user authentication and session creation.
    Local imports are used to break circular dependency.
    """
    from booking_system import get_mentors_and_peers
    from shared import list_workshops, list_mentors
    global session, user_uid

    create_session()
    if session is not None and user_uid is not None:
        # Get 2D list for both mentors and peers
        mentors, peers = get_mentors_and_peers()

        # List all available mentors and upcoming workshops from firebase
        list_mentors(mentors)
        list_workshops()
    else:
        click.secho("Please sign in to view workshops...", fg="orange", blink=True)


@main.command(name="request_session")
def request_session():
    """Requests a meeting with a mentor.
    
    This function requires user authentication and session creation.
    """
    from booking_system import request_meeting
    global session, user_uid
    
    if session is not None and user_uid is not None:
        user = auth.get_user(uid=user_uid)
        request_meeting(user.email)
    else:
        click.secho("Please sign in to request a session...", fg="orange", blink=True)


if __name__ == "__main__":
    main()