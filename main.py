import firebase_admin
from firebase_admin import credentials, db
from authentication import login, sign_up
import click


def connect_to_database():
    """Connect to Firebase Database"""
    cred = credentials.Certificate("skillsync-project-451208-firebase-adminsdk-fbsvc-247be52390.json")
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://skillsync-project-451208-default-rtdb.firebaseio.com/"
    })


@click.group()
def main():
    """Main entry point for the CLI"""
    connect_to_database()


@main.command()
@click.option("--returning_user", prompt="Are you a returning user?[y/n]", type=str)
def authenticate(returning_user):
    """Handles user authentication based on returning status."""
    if returning_user.lower() == "y":
        login()
    elif returning_user.lower() == "n":
        sign_up()
    else:
        click.secho(f"Invalid option '{returning_user}', please enter 'y' or 'n'", fg="red")


if __name__ == "__main__":
    main()