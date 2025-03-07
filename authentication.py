from firebase_admin import db
from firebase_admin import auth
from shared import read_from_database, validate_not_empty
import click


def create_user_in_firebase(first_name:str, email:str, role:str, password:int, expertise:str):
    """Handles user authentication based on returning status."""
    try:
        user = auth.create_user(
            display_name = first_name,
            email = email,
            password = password,
        )

        try: 
            ref = db.reference(f"/Users/{user.uid}")
            user_data = {
                "first_name": first_name,
                "email": email,
                "role": role,
                "expertise": expertise,
            }

            ref.set(user_data)
        except ValueError:
            click.secho("The file path does not exist or the app is invalid...", fg="red")
    except:
        click.secho("Error: failed to create user...", fg="red")


def login():
    """Handles user login"""
    click.secho("Logging in...", fg="yellow")

    email = click.prompt("Enter your email")
    password = click.prompt("Enter your password", hide_input=True, confirmation_prompt=True)

    try:
        user = auth.get_user_by_email(email)
        full_name = read_from_database(f"/Users/{user.uid}/first_name")
        click.secho(f"\nWelcome, {full_name}. You have successfully signed in.", bg="yellow", underline=True)

        return user.uid
    except ValueError:
        click.secho("Email was empty, none, or malformed....", fg="red", blink=True)
    except auth.UserNotFoundError:
        click.secho("Error: user does not exist....", fg="red", bold=True)
    except:
        click.secho("Error while retrieving user from firebase....", fg="red")
    

# @cli.command()
def sign_up():
    """Handles user sign-up"""
    click.secho("Signing up...", blink=True, fg="yellow")

    firstname = click.prompt("Enter first name")
    email = click.prompt("Enter your email")
    password = click.prompt("Enter your password", hide_input=True, confirmation_prompt=True)
    role = click.prompt("What role are you taking up?", type=click.Choice(["mentor","peer"], case_sensitive=True))
    expertise = click.prompt("What is your expertise?")

    try:
        user_id = create_user_in_firebase(firstname, email, role, password, expertise)
        click.secho("Account created successfully!", fg="green")

        return user_id
    except auth.EmailAlreadyExistsError:
        click.secho("Error: email already exists", fg="red")
    except:
        click.secho("Error signing up")