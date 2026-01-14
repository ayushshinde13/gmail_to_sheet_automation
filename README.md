# gmail_to_sheet_automation
# Gmail to Google Sheets Integration

A Python-based application that extracts Gmail messages and syncs them into Google Sheets using Google APIs. The project includes a Flask-based web interface for manual synchronization.

---

## Features
- Gmail API integration
- Google Sheets API integration
- Flask web interface
- One-click email sync
- Clears and rewrites sheet data for fresh sync
- Secure credential handling

---

## Tech Stack
- Python
- Flask
- Gmail API
- Google Sheets API

---

## Project Architecture
- `gmail_service.py`: Fetches emails from Gmail
- `sheets_service.py`: Writes email data to Google Sheets
- `app.py`: Flask web interface
- `templates/`: UI files

---

## Setup Instructions

1. Clone the repository
```bash
git clone https://github.com/ayushshinde13/gmail-to-sheets.git
cd gmail-to-sheets

