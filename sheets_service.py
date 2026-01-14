from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def get_sheets_service():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("sheets", "v4", credentials=creds)


def write_to_sheet(service, emails, spreadsheet_id):
    sheet_name = "Sheet1"

    # 1️⃣ CLEAR ENTIRE SHEET
    service.spreadsheets().values().clear(
        spreadsheetId=spreadsheet_id,
        range=f"{sheet_name}!A1:Z"
    ).execute()

    # 2️⃣ HEADER ROW
    values = [
        ["From", "Email", "Subject", "Date", "Content"]
    ]

    # 3️⃣ EMAIL DATA
    for email in emails:
        values.append([
            email.get("from", ""),
            email.get("email", ""),
            email.get("subject", ""),
            email.get("date", ""),
            email.get("content", "")
        ])

    body = {"values": values}

    # 4️⃣ WRITE FRESH DATA
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"{sheet_name}!A1",
        valueInputOption="RAW",
        body=body
    ).execute()
