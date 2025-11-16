from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import json


SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.events'
]

CREDENTIALS_FILE = 'credentials.json'  
TOKEN_FILE = 'creds.json'  

def get_credentials():
    """
    Get valid user credentials from storage or initiate OAuth2 flow.
    
    If credentials don't exist or are invalid, this will:
    1. Open a browser window
    2. Ask the user to authorize the app with their Google account
    3. Store the credentials in creds.json for future use
    
    Returns:
        Credentials object for making API calls
    """
    creds = None
    
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, 'r') as token:
                creds_data = json.load(token)
                creds = Credentials.from_authorized_user_info(creds_data, SCOPES)
        except Exception as e:
            print(f"Error loading credentials: {e}")
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired credentials...")
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing credentials: {e}")
                creds = None
        

        if not creds:
            if not os.path.exists(CREDENTIALS_FILE):
                print(f"Error: {CREDENTIALS_FILE} not found!")
                print("Please download OAuth 2.0 credentials from Google Cloud Console")
                print("Visit: https://console.cloud.google.com/apis/credentials")
                raise FileNotFoundError(f"{CREDENTIALS_FILE} not found")
            
            print("Opening browser for Google authentication...")
            print("Please authorize this application in your browser.")
            
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
            
            print("Authentication successful!")
        

        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
            print(f"Credentials saved to {TOKEN_FILE}")
    
    return creds
