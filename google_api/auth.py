from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
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
            self.wfile.write(b"<html><body><h2>Authentication complete. You can close this window.</h2></body></html>")
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
    BACKEND_URL = "http://37.27.51.34:42679/"
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

        try:
            exch_data = exch.json()
        except ValueError:
            exch_data = None

        creds_data = None
        if isinstance(exch_data, dict):
            creds_data = exch_data.get("creds") or exch_data.get("token") or exch_data

        if creds_data:
            with open(TOKEN_FILE, "w") as token:
                json.dump(creds_data, token)
        elif not os.path.exists(TOKEN_FILE):
            raise FileNotFoundError(f"{TOKEN_FILE} not found after backend exchange")

        with open(TOKEN_FILE, "r") as token:
            creds_data = json.load(token)
            creds = Credentials.from_authorized_user_info(creds_data, SCOPES)
        return creds
