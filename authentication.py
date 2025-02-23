from firebase_admin import db
from firebase_admin import auth
from shared import read_from_database
import click


@click.group()
def cli():
    """User authentication commands"""
    pass


def create_user_in_firebase(first_name:str, email:str, role:str, password:int, expertise:str):
    """Handles user authentication based on returning status."""
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


@cli.command()
@click.option("--email", prompt="Enter your email")
@click.option("--password", prompt="Enter your password", hide_input=True, confirmation_prompt=True)
def login(email, password):
    """Handles user login"""
    click.echo("Logging in...")

    try:
        user = auth.get_user_by_email(email)
        full_name = read_from_database(f"/Users/{user.uid}/first_name")
        click.echo(f"\nWelcome, {full_name}. You have successfully signed in.")
    except auth.UserNotFoundError:
        click.secho("Error: user does not exist", fg="red")
    

@cli.command()
@click.option("--firstname", prompt="Enter first name")
@click.option("--email", prompt="Enter your email")
@click.option("--password", prompt="Enter your password", hide_input=True, confirmation_prompt=True)
@click.option("--role", prompt="What role are you taking up? [mentor/peer]")
@click.option("--expertise", prompt="What is your expertise?")
def sign_up(firstname, email, password, role, expertise):
    """Handles user sign-up"""
    click.echo("Signing up...")

    try:
        create_user_in_firebase(firstname, email, role, password, expertise)
        click.echo("Account created successfully!")
    except auth.EmailAlreadyExistsError:
        click.secho("Error: email already exists", fg="red")


if __name__ == "__main__":
    cli()