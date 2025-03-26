from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from datetime import datetime
import click

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_credentials():
    creds = None

    # Check if token.json exists and load credentials
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # Refresh or reauthenticate if credentials are invalid
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing token: {e}")
        else:
            try:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)
            except FileNotFoundError:
                print("Error: 'credentials.json' file not found.")
                return None
            except Exception as e:
                print(f"Error during reauthentication: {e}")
                return None

        # Save refreshed or new credentials to token.json
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds


def create_calendar_event(email1, email2, summary, event_date, start_time, end_time):
    creds = get_credentials()
    if not creds:
        print("Failed to obtain valid credentials. Exiting...")
        return None

    try:
        service = build("calendar", "v3", credentials=creds)

        # Parse event date and prepare API-compatible format
        event_date = datetime.strptime(event_date, "%Y-%m-%d")
        print(f"Creating event on: {event_date.strftime('%Y-%m-%d')}")

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

        # Insert the event and handle API response
        event = service.events().insert(calendarId='primary', body=event).execute()
        click.echo(f"Event created: {event.get('htmlLink')}")
        return event.get("id")

    except HttpError as error:
        print(f"An error occurred with the Calendar API: {error}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return None
