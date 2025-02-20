import firebase_admin
from firebase_admin import credentials, db
from authentication import login, sign_up


def connect_to_database():
    cred = credentials.Certificate("skillsync-project-451208-firebase-adminsdk-fbsvc-247be52390.json")
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://skillsync-project-451208-default-rtdb.firebaseio.com/"
    })


def main():
    # Connect to the databade first
    connect_to_database()
    returning_user = input("Are you a returning user?[y/n] ").strip().lower()

    if returning_user == "y":
        login()
    elif returning_user == "n":
        sign_up()


# main()