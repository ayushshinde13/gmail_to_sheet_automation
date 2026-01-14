from gmail_service import get_gmail_service
from email_parser import fetch_emails
from sheets_service import get_sheets_service, write_to_sheet
from config import SPREADSHEET_ID


def main():
    print("🔐 Authenticating Gmail...")
    gmail_service = get_gmail_service()
    print(type(gmail_service))


    print("📩 Fetching emails...")
    emails = fetch_emails(gmail_service)

    if not emails:
        print("⚠️ No emails found.")
        return

    print("📊 Writing data to Google Sheet...")
    sheets_service = get_sheets_service()

    write_to_sheet(sheets_service,emails, SPREADSHEET_ID)

    print("✅ Done! Emails pushed to Google Sheets.")


if __name__ == "__main__":
    main()
