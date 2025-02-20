from firebase_admin import db
from firebase_admin import auth
from shared import read_from_database
import click

def login():
    print("Log in...")
    email = input("\nEnter email: ")
    password = input("Enter password: ")

    try:
        guy = auth.get_user_by_email(email)
        print(f"\nWelcome, {read_from_database(f'/Users/{guy.uid}/full_name')}. You have succesfully signed in.....")
        # print(read_from_database(f"/Users/{guy.uid}"))
    except auth.UserNotFoundError:
        print("Error: user does not exist")
    
@click.command()
# click.echo(click.style(f"I am colored {color}", fg=color))
def sign_up():
    print("Sign up here.....")
    email = input("\nEnter email: ").strip()
    password = input("Enter password: ").strip()
    first_name = input("Enter first name: ").strip()
     
    # Prompt the user for a role
    role = input("What role are you taking up?[mentor/peer'] ").strip().lower()
    expertise = input("What is your expertise?: ").strip().lower()

    try:
        authenticate_user(first_name, email, role, password, expertise)
    except auth.EmailAlreadyExistsError:
        print("Error: email already exists")


def authenticate_user(first_name:str, email:str, role:str, password:int, expertise:str):
    user = auth.create_user(
        display_name = first_name,
        email = email,
        password = password,
    )
    
    ref = db.reference(f"/Users/{user.uid}")
    user_data = {
        "first_name": first_name,
        "email": email,
        "role": role,
        "expertise": expertise,
    }
    print(f"{user_data}")
    ref.set(user_data)