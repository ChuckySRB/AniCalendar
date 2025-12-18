import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)

def add_anime_event(service, anime_title: str, start_timestamp: int, total_episodes: int, anilist_id: int, have_airing_time: str):
    """
    Adds a recurring event to Google Calendar or updates it if a specific time is now available.
    """
    # 1. Calculate new timing
    start_dt = datetime.datetime.fromtimestamp(start_timestamp) + datetime.timedelta(minutes=30)
    end_dt = start_dt + datetime.timedelta(minutes=23)

    # Convert the boolean to a string because Google Extended Properties only store strings
    have_airing_time_str = str(have_airing_time).lower()

    # 2. Check for existing event
    page_token = None
    existing_event = None

    while True:
        events_result = service.events().list(
            calendarId='primary', 
            privateExtendedProperty=f'anilist_id={anilist_id}',
            pageToken=page_token).execute()
        
        items = events_result.get('items', [])
        if items:
            existing_event = items[0] # Take the first match
            break
            
        page_token = events_result.get('nextPageToken')
        if not page_token:
            break

    # 3. Logic: Update existing event or Create new one
    if existing_event:
        # Get the old 'had_airing_time' value from the calendar
        properties = existing_event.get('extendedProperties', {}).get('private', {})
        stored_had_time = properties.get('had_airing_time', 'false').lower()

        # Update only if: Old event had no time (false) AND New data has time (true)
        if stored_had_time == 'false' and have_airing_time_str == 'true':
            print(f"Updating time for: {anime_title} (Precise time now available)")
            
            updated_fields = {
                'start': {'dateTime': start_dt.isoformat(), 'timeZone': 'UTC'},
                'end': {'dateTime': end_dt.isoformat(), 'timeZone': 'UTC'},
                'extendedProperties': {
                    'private': {
                        'anilist_id': str(anilist_id),
                        'had_airing_time': 'true' # Mark it as updated
                    }
                }
            }
            
            # Use patch to only update specific fields without overwriting everything
            service.events().patch(
                calendarId='primary', 
                eventId=existing_event['id'], 
                body=updated_fields
            ).execute()
            return
        else:
            print(f"Skipping: {anime_title} is already on the calendar correctly.")
            return

    # 4. Create the Event (If no existing event was found)
    event_body = {
        'summary': f'[Anime] {anime_title}',
        'description': f'Automatically added from AniList. ID: {anilist_id}',
        'colorId': '11', 
        'start': {
            'dateTime': start_dt.isoformat(),
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_dt.isoformat(),
            'timeZone': 'UTC',
        },
        'recurrence': [
            f'RRULE:FREQ=WEEKLY;COUNT={total_episodes}'
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [{'method': 'popup', 'minutes': 0}],
        },
        'extendedProperties': {
            'private': {
                'anilist_id': str(anilist_id),
                'had_airing_time': have_airing_time_str
            }
        }
    }

    created_event = service.events().insert(calendarId='primary', body=event_body).execute()
    print(f"Event created: {created_event.get('htmlLink')}")