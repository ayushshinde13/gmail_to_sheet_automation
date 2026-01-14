import base64
import re
from email.utils import parsedate_to_datetime


def parse_email(message):
    headers = message["payload"]["headers"]

    # ✅ Use lowercase keys everywhere (best practice)
    email_data = {
        "from": "",
        "email": "",
        "subject": "",
        "date": "",
        "content": ""
    }

    for header in headers:
        name = header["name"].lower()
        value = header["value"]

        if name == "from":
            email_data["from"] = value

            # extract email address
            match = re.search(r"<(.+?)>", value)
            if match:
                email_data["email"] = match.group(1)
            else:
                email_data["email"] = value

        elif name == "subject":
            email_data["subject"] = value

        elif name == "date":
            email_data["date"] = parsedate_to_datetime(value).strftime(
                "%Y-%m-%d %H:%M:%S"
            )

    def extract_body(payload):
        if payload.get("body", {}).get("data"):
            return base64.urlsafe_b64decode(
                payload["body"]["data"]
            ).decode("utf-8", errors="ignore")

        for part in payload.get("parts", []):
            if part.get("mimeType") == "text/plain" and part["body"].get("data"):
                return base64.urlsafe_b64decode(
                    part["body"]["data"]
                ).decode("utf-8", errors="ignore")

        return ""

    # ✅ store body as content
    email_data["content"] = extract_body(message["payload"])
    return email_data


def fetch_emails(service, max_results=5):
    """
    Fetch emails from Gmail and return parsed emails
    """
    results = service.users().messages().list(
        userId="me",
        maxResults=max_results,
        labelIds=["INBOX"]
    ).execute()

    messages = results.get("messages", [])
    parsed_emails = []

    for msg in messages:
        msg_data = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="full"
        ).execute()

        parsed_emails.append(parse_email(msg_data))

    return parsed_emails
