from firebase_admin import db
from firebase_admin import auth
from shared import read_from_database
import click

@click.command()
@click.option("--email", prompt="Enter your email")
@click.option("--password", prompt="Enter your password", hide_input=True, confirmation_prompt=True)
def login(email, password):
    click.echo("Log in...")
    # email = input("\nEnter email: ")
    # password = input("Enter password: ")
    try:
        guy = auth.get_user_by_email(email)
        click.echo(f"\nWelcome, {read_from_database(f'/Users/{guy.uid}/full_name')}. You have succesfully signed in.....")
    except auth.UserNotFoundError:
        click.echo("Error: user does not exist")
    

@click.command()
@click.option("--email", prompt="Enter your email")
@click.option("--password", prompt="Enter your password", hide_input=True, confirmation_prompt=True)
@click.option("--firstname", prompt="Enter first name")
@click.option("--role", prompt="What role are you taking up?[mentor/peer']")
@click.option("--expertise", prompt="What is your expertise?")
def sign_up(email, password, firstname, role, expertise):
    click.echo("Sign up here.....")
    # email = input("\nEnter email: ").strip()
    # password = input("Enter password: ").strip()
    # first_name = input("Enter first name: ").strip()
     
    # Prompt the user for a role
    # role = input("What role are you taking up?[mentor/peer'] ").strip().lower()
    # expertise = input("What is your expertise?: ").strip().lower()

    try:
        authenticate_user(firstname, email, role, password, expertise)
    except auth.EmailAlreadyExistsError:
        click.echo("Error: email already exists")

@click.command()
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
    click.echo(f"{user_data}")
    ref.set(user_data)