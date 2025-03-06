import click
from authentication import login, sign_up
from database import connect_to_database


@click.group()
def main():
    """Main entry point for the CLI"""
    connect_to_database()


@main.command()
def authenticate():
    """Handles user authentication based on returning status."""
    returning_user = click.prompt("Are you a returning user? [y/n]", type=click.Choice(["y", "n"], case_sensitive=True))
    if returning_user == "y":
        login()
    else:
        sign_up()


@main.command()
def view_workshops():
    """This function will list upcoming workshops as well as menotrs available for booking. 
    The local imports are to break circular dependency.
    """
    from booking_system import get_mentors_and_peers
    from shared import list_workshops, list_mentors

    # Get 2D list for both mentors and peers
    mentors, peers = get_mentors_and_peers()

    # List all available mentors and upcoming workshops from firebase
    list_mentors(mentors)
    list_workshops()


# @main.command()
# def end_session():
#     cookies = auth.create_session_cookie()


@main.command()
def request_session():
    from booking_system import request_meeting


if __name__ == "__main__":
    main()