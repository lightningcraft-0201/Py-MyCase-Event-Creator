import json
import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
from settings import CREDENTIALS_PATH, SCOPES, SHEET_SCOPES, GOOGLE_SHEETS_CREDENTIALS_PATH

def authenticate_gmail():
    creds = None
    
    # Check if token.json exists and load credentials
    if os.path.exists('token.json'):
        with open('token.json', 'r') as token:
            creds = Credentials.from_authorized_user_info(json.load(token), SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                # Save the refreshed token
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())
            except Exception as e:
                print(f"Failed to refresh token: {e}")
                return None
        else:
            try:
                flow = InstalledAppFlow.from_client_config(CREDENTIALS_PATH, SCOPES)
                creds = flow.run_local_server(port=0)
                # Save the new token
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())
            except Exception as e:
                print(f"Failed to complete OAuth flow: {e}")
                return None

    # Build the Gmail service
    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except Exception as e:
        print(f"Failed to build Gmail service: {e}")
        return None
