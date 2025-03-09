import os.path, click

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from firebase_admin import db, auth
from datetime import datetime

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_credentials():
    creds = None
  
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    
    return creds


def create_calender_event(email1, email2, summary, event_date, start_time, end_time):
    creds = get_credentials()
    user = auth.get_user_by_email(email1)

    service = build("calendar", "v3", credentials=creds)
    event_date = datetime.strptime(event_date, "%Y-%m-%d")

    event = {
        'summary': summary,
        "start": {
            "dateTime": f"{event_date.strftime('%Y-%m-%d')}T{start_time}:00",
            "timeZone": "Africa/Johannesburg",
        },
        'end': {
            "dateTime": f"{event_date.strftime('%Y-%m-%d')}T{end_time}:00",
            "timeZone": "Africa/Johannesburg",
        },
        'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=2'
        ],
        'attendees': [
            {'email': email1},
            {'email': email2}
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
            {'method': 'email', 'minutes': 24 * 60},
            {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    click.echo(f"Event created: {event.get('htmlLink')}")

    return event.get("id")
