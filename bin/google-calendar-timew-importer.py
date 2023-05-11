import os
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
#from timew import TimeWarrior

SCOPES = ['https://www.googleapis.com/auth/calendar']
creds_file = '/home/szacun/Downloads/client_secret_607081677527-9blculhrb2ths67gpkh14jkrkh18hbcn.apps.googleusercontent.com.json'

creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/calendar'])
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            creds_file, SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())


service = build('calendar', 'v3', credentials=creds)

# Set up TimeWarrior client
#timew = TimeWarrior()

# Set up start and end date for event query
start_date = datetime.utcnow().isoformat() + 'Z'  # Current date and time in UTC
end_date = (datetime.utcnow() + timedelta(days=7)).isoformat() + 'Z'  # 7 days from now in UTC

# Get events from Google Calendar API
events_result = service.events().list(calendarId='primary', timeMin=start_date, timeMax=end_date, singleEvents=True, orderBy='startTime').execute()
events = events_result.get('items', [])

# Loop through events and add to TimeWarrior
for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    end = event['end'].get('dateTime', event['end'].get('date'))
    summary = event['summary']
    timew_command = f'timew track "{summary}" from {start} to {end}'
    print(timew_command)
