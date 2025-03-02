from firebase_admin import db
from firebase_admin import auth
from shared import read_from_database, validate_not_empty
import click


@click.group()
def cli():
    """User authentication commands"""
    pass


def create_user_in_firebase(first_name:str, email:str, role:str, password:int, expertise:str):
    """Handles user authentication based on returning status."""
    try:
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

        ref.set(user_data)
    except auth.EmailAlreadyExistsError:
        click.secho("Error: Email already exists", fg="red")


@cli.command()
def login():
    """Handles user login"""
    click.echo("Logging in...")

    email = click.option("--email", prompt="Enter your email")
    password = click.option("--password", prompt="Enter your password", hide_input=True, confirmation_prompt=True)

    try:
        user = auth.get_user_by_email(email)
        full_name = read_from_database(f"/Users/{user.uid}/first_name")
        click.echo(f"\nWelcome, {full_name}. You have successfully signed in.")
    except auth.UserNotFoundError:
        click.secho("Error: user does not exist", fg="red")
    

@cli.command()
def sign_up():
    """Handles user sign-up"""
    click.echo("Signing up...")

    firstname = click.option("--firstname", prompt="Enter first name")
    email = click.option("--email", prompt="Enter your email")
    password = click.option("--password", prompt="Enter your password", hide_input=True, confirmation_prompt=True)
    role = click.option("--role", prompt="What role are you taking up? [mentor/peer]")
    expertise = click.option("--expertise", prompt="What is your expertise?")

    try:
        create_user_in_firebase(firstname, email, role, password, expertise)
        click.echo("Account created successfully!")
    except auth.EmailAlreadyExistsError:
        click.secho("Error: email already exists", fg="red")
    except:
        click.secho("Error signing up")


if __name__ == "__main__":
    cli()