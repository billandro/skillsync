import firebase_admin
import os
from dotenv import load_dotenv
from firebase_admin import credentials

# Load environment variables from .env file
load_dotenv()

def connect_to_database():
    """Connect to Firebase Database"""
    cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if cred_path is None:
        raise Exception("Service account credentials not found. Please set the GOOGLE_APPLICATION_CREDENTIALS environment variable.")

    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://skillsync-project-451208-default-rtdb.firebaseio.com/"
    })