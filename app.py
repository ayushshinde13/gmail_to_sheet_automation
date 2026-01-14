from flask import Flask, render_template, request
from src.gmail_service import get_gmail_service
from src.email_parser import fetch_emails
from src.sheets_service import get_sheets_service, write_to_sheet

app = Flask(__name__)

SPREADSHEET_ID = "1zsBAA-g-gdjD6bM_sUNjQ1hzfucQ4QK5etf7qPzm4aE"

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""

    if request.method == "POST":
        count = int(request.form.get("count", 5))

        gmail_service = get_gmail_service()
        sheets_service = get_sheets_service()

        emails = fetch_emails(gmail_service, count)
        write_to_sheet(sheets_service, emails, SPREADSHEET_ID)

        message = f"{len(emails)} emails synced successfully!"

    return render_template("index.html", message=message)

if __name__ == "__main__":
    app.run(debug=True)
