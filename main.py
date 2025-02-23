import firebase_admin
from firebase_admin import credentials, db
from authentication import login, sign_up
import click


def connect_to_database():
    cred = credentials.Certificate("skillsync-project-451208-firebase-adminsdk-fbsvc-247be52390.json")
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://skillsync-project-451208-default-rtdb.firebaseio.com/"
    })


@click.command()
@click.option("--returning_user", prompt="Are you a returning user?[y/n]")
def main(returning_user):
    # Connect to the databade first
    connect_to_database()
    # returning_user = input("Are you a returning user?[y/n] ").strip().lower()

    if returning_user == "y":
        login()
    elif returning_user == "n":
        sign_up()
    else:
        click.echo("You entered the invalid option '{}'".format(returning_user))


# main()