from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from google.auth.transport.requests import Request
import os.path
import time

import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict

SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    #'https://www.googleapis.com/auth/calendar.events,'
    'https://www.googleapis.com/auth/tasks'
]

CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), '..', 'credentials.json')
TOKEN_FILE = os.path.join(os.path.dirname(__file__), '..', 'creds.json')  

OAUTH_STATE = {}

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# store short-lived states
_state_store: Dict[str, float] = {}

class ExchangeRequest(BaseModel):
    code: str
    state: str

def authorize():
    flow = Flow.from_client_secrets_file(
        CREDENTIALS_FILE, scopes=SCOPES, redirect_uri="http://127.0.0.1:8080/"
    )
    auth_url, state = flow.authorization_url(
        prompt="consent", access_type="offline", include_granted_scopes="true"
    )
    OAUTH_STATE[state] = time.time()
    return {"auth_url": auth_url, "state": state}

@app.get("/authorize")
def fastapi_authorize():
    if not os.path.exists(CREDENTIALS_FILE):
        raise HTTPException(status_code=500, detail=f"{CREDENTIALS_FILE} not found on server")
    flow = Flow.from_client_secrets_file(
        CREDENTIALS_FILE,
        scopes=SCOPES,
        redirect_uri="http://127.0.0.1:8080/"
    )
    auth_url, state = flow.authorization_url(prompt="consent", access_type="offline", include_granted_scopes="true")
    _state_store[state] = time.time()
    return {"auth_url": auth_url, "state": state}

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

        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
            print(f"Credentials saved to {TOKEN_FILE}")
    
    return creds

@app.post("/exchange_code")
def exchange_code(req: ExchangeRequest):
    if req.state not in _state_store:
        raise HTTPException(status_code=400, detail="Invalid or expired state")
    # optional: remove state
    _state_store.pop(req.state, None)

    flow = Flow.from_client_secrets_file(
        CREDENTIALS_FILE,
        scopes=SCOPES,
        redirect_uri="http://127.0.0.1:8080/"
    )
    try:
        flow.fetch_token(code=req.code)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch token: {e}")

    creds = flow.credentials
    with open(TOKEN_FILE, "w") as f:
        f.write(creds.to_json())

    return {"status": "ok"}
