from firebase_admin import db
import firebase_admin.auth as auth
import click, requests


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
            click.secho("Account created successfully!", fg="green")
        except ValueError:
            click.secho("The file path does not exist or the app is invalid...", fg="red")
    except:
        click.secho("Error: failed to create user...", fg="red")


def login():
    """Handles user login"""
    click.secho("Logging in...", fg="yellow")

    email = click.prompt("Enter your email")
    password = click.prompt("Enter your password", hide_input=True, confirmation_prompt=True)

    api_key = "AIzaSyDvWCvCBT37F2nttDjfddsAE3Wo-Sh4sd8"
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    try:
        response = requests.post(url, json=payload)
        response_data = response.json()

        if "idToken" in response_data:
            uid = response_data.get("localId")
            click.secho(f"\nWelcome! You have successfully signed in.", bg="yellow", underline=True)
            return response_data["idToken"], uid
        else:
            click.secho(f"Error: {response_data.get('error', {}).get('message', 'Unknown error')}", fg="red", bold=True)
            return None, None

    except requests.RequestException as e:
        click.secho(f"Error while retrieving user from Firebase", fg="red")
        return None, None
    

def sign_up():
    """Handles user sign-up"""
    click.secho("Signing up...", fg="yellow")

    firstname = click.prompt("Enter first name")
    email = click.prompt("Enter your email")
    password = click.prompt("Enter your password", hide_input=True, confirmation_prompt=True)
    role = click.prompt("What role are you taking up?", type=click.Choice(["mentor","peer"], case_sensitive=True))
    expertise = click.prompt("What is your expertise?")

    api_key = "AIzaSyDvWCvCBT37F2nttDjfddsAE3Wo-Sh4sd8"
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    try:
        create_user_in_firebase(firstname, email, role, password, expertise)
        try:
            response = requests.post(url, json=payload)
            response_data = response.json()

            if "idToken" in response_data:
                uid = response_data.get("localId")
                click.secho(f"\nWelcome! You have successfully signed up.", bg="yellow", underline=True)
                return response_data["idToken"], uid
            else:
                click.secho(f"Error: {response_data.get('error', {}).get('message', 'Unknown error')}", fg="red", bold=True)
                return None, None
            
        except requests.RequestException as e:
            click.secho(f"Error while retrieving user from Firebase: {e}", fg="red")
            return None, None
    except auth.EmailAlreadyExistsError:
        click.secho("Error: email already exists", fg="red")
    except:
        click.secho("Error signing up", fg="red")