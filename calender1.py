import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Utility function to save credentials
def save_credentials(creds):
    # Save credentials with refresh token to token.json
    token_data = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": creds.scopes,
        "expiry": creds.expiry.isoformat() if creds.expiry else None
    }
    with open("token.json", "w") as token:
        json.dump(token_data, token)


# Utility function to authenticate user
def authenticate_user():
    # Perform reauthentication flow
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)
    save_credentials(creds)
    return creds


# Function to retrieve credentials, refresh if expired, or reauthenticate
def get_credentials():
    creds = None
    try:
        # Load existing token
        with open("token.json", "r") as token:
            creds = Credentials.from_authorized_user_info(json.load(token), SCOPES)
        
        # Refresh token if expired
        if not creds.valid or creds.expired:
            creds.refresh(Request())
            save_credentials(creds)  # Save updated token
    except Exception as e:
        print(f"Error loading credentials: {e}. Triggering authentication flow.")
        creds = authenticate_user()

    return creds

# Function to create a calendar event
def create_calendar_event(email1, email2, summary, event_date, start_time, end_time):
    # Validate attendee emails
    if not email1 or not email2 or "@" not in email1 or "@" not in email2:
        raise ValueError("Invalid attendee email format. Please use valid email addresses.")

    # Build the Google Calendar service
    service = build("calendar", "v3", credentials=get_credentials())

    # Define the event details
    event = {
        "summary": summary,
        "description": f"A meeting with {email1} and {email2}.",
        "start": {
            "dateTime": f"{event_date}T{start_time}:00",
            "timeZone": "Africa/Johannesburg",
        },
        "end": {
            "dateTime": f"{event_date}T{end_time}:00",
            "timeZone": "Africa/Johannesburg",
        },
        "attendees": [
            {"email": email1},
            {"email": email2}
        ],
    }

    try:
        # Insert the event into the calendar
        event_result = service.events().insert(calendarId="primary", body=event).execute()
        return event_result["id"]
    except Exception as e:
        print(f"Failed to create the event: {e}")
        raise
