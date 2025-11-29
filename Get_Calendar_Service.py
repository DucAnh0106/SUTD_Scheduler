#These are the libraries for talking to Google APIs to upload the data
import os
import sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_application_path():
    """ Returns the path of the .exe folder if frozen, else script folder """
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def get_calendar_service():
    creds = None
    
    # 1. Get the path where the .exe is located
    base_path = get_application_path()
    
    # 2. Define full paths for token and credentials
    token_path = os.path.join(base_path, 'token.json')
    creds_path = os.path.join(base_path, 'credentials.json')

    # 3. Check for token
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(creds_path):
                raise FileNotFoundError(f"Could not find credentials.json at: {creds_path}")
                
            flow = InstalledAppFlow.from_client_secrets_file(
                creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
            
        # 4. Save token to the .exe folder (not the temp folder)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

#This function is for uploading the extracted and cleaned data onto Google calendar
def get_calendar_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    # It is created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Token exists but expired - refresh it
            creds.refresh(Request())
        else:
            # No token exists - do new login
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0, open_browser=True)
            
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

    # Build the service object (this is what talks to Google)
    service = build('calendar', 'v3', credentials=creds)
    return service
