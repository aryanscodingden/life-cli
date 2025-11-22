from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import json
import os
import webbrowser
import http.server
import threading
import urllib.parse
import requests

SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/tasks'
]

CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'creds.json'

LOCAL_CALLBACK_PORT = 8080

def _run_local_server(timeout=300):
    class Handler(http.server.BaseHTTPRequestHandler):
        server_data = {"code": None, "state": None}
        server_event = threading.Event()

        def do_GET(self):
            qs = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(qs)
            self.__class__.server_data["code"] = params.get("code", [None])[0]
            self.__class__.server_data["state"] = params.get("state", [None])[0]
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body>Authentication complete. You can close this window.</body></html>")
            self.__class__.server_event.set()

        def log_message(self, *args):
            return

    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", LOCAL_CALLBACK_PORT), Handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    waited = Handler.server_event.wait(timeout)
    code = Handler.server_data.get("code")
    state = Handler.server_data.get("state")
    try:
        httpd.shutdown()
        httpd.server_close()
    except Exception:
        pass
    return code, state

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
    BACKEND_URL = "http://localhost:8000"
    creds = None

    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, 'r') as token:
                creds_data = json.load(token)
                creds = Credentials.from_authorized_user_info(creds_data, SCOPES)
        except Exception:
            creds = None

    if creds and creds.valid:
        return creds

    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            with open(TOKEN_FILE, "w") as token:
                token.write(creds.to_json())
            return creds
        except Exception:
            creds = None

    if BACKEND_URL:
        resp = requests.get(f"{BACKEND_URL}/authorize", timeout=60)
        resp.raise_for_status()
        data = resp.json()
        auth_url = data["auth_url"]
        expected_state = data.get("state")

        webbrowser.open(auth_url)
        print("Opened browser for authentication. Waiting for callback...")

        code, returned_state = _run_local_server()
        if not code:
            raise RuntimeError("Timed out waiting for OAuth callback code")

        state_to_send = returned_state or expected_state
        exch = requests.post(f"{BACKEND_URL.rstrip('/')}/exchange_code", json={"code": code, "state": state_to_send}, timeout=10)
        exch.raise_for_status()
        if not os.path.exists(TOKEN_FILE):
            raise FileNotFoundError(f"{TOKEN_FILE} not found after backend exchange")
        with open(TOKEN_FILE, "r") as token:
            creds_data = json.load(token)
            creds = Credentials.from_authorized_user_info(creds_data, SCOPES)
        return creds

    if not os.path.exists(CREDENTIALS_FILE):
        raise FileNotFoundError(f"{CREDENTIALS_FILE} not found")
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
    creds = flow.run_local_server(port=0)
    with open(TOKEN_FILE, 'w') as token:
        token.write(creds.to_json())
    return creds