
# Automated Email Parsing and Legal Case Management Integration

## Overview

The script automatically logs into a Gmail account, retrieves emails, extracts relevant case information, and logs it into a specified Google Sheet. Additionally, it interacts with a legal case management platform to create events and reminders based on the extracted data. This process minimizes manual entry errors and saves time by automating routine data capture and entry tasks.

## Video Preview

[![Video Preview](https://github.com/zima-0201/Project-Images/blob/main/video%20preview/Py-MyCase-Event-Creator.jpeg)](https://brand-car.s3.eu-north-1.amazonaws.com/Four+Seasons/Py-Youtube-Downloader.mp4)


## Features

- **Email Extraction**: Scans Gmail for new emails in specific categories and extracts pertinent information.
- **Data Processing**: Parses email content to retrieve details such as case number, event type, scheduled dates, etc.
- **Google Sheets Integration**: Automatically logs data into a Google Sheet for record-keeping and further processing.
- **Case Management Integration**: Utilizes Selenium to log into a case management platform and schedules new events based on email data.
- **Automated Scheduling**: The script runs automatically at a scheduled time each day to ensure all new data is captured without manual intervention.

## Prerequisites

To run this script, you will need:

- Python 3.8 or higher
- Access to a Gmail account with applicable credentials
- Access to a Google Sheets spreadsheet
- Credentials for the legal case management platform
- ChromeDriver and Selenium installed for automated web interactions

## Setup

1. **Environment Setup**:
   Clone the repository and install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. **Credentials Configuration**:
   Ensure you have `credentials.json` for Google API and `token.json` for stored credentials. Place these files in the root directory.

3. **Google Sheets Setup**:
   Update `GOOGLE_SHEETS_CREDENTIALS` in the script to match your Google Sheets API credentials.

4. **Environment Variables**:
   Define necessary environment variables such as `USER_NAME` and `USER_PASS` for the case management platform login.

## Usage

To run the script manually, execute:

```bash
python automated_case_management.py
```

To ensure the script runs at a scheduled time every day, it is configured to trigger at 04:00 AM automatically. Adjust this time by modifying the `schedule` call in the script as needed.

## Automated Tasks

- **Email Fetching**: Connects to Gmail and fetches new emails.
- **Data Extraction and Logging**: Extracts data from emails and logs it into a Google Sheet.
- **Event Creation in Case Management Platform**: Logs into the case management system and creates events.

## Troubleshooting

- **Common Issues**:
  - Invalid credentials: Ensure your Google API credentials are correct and valid.
  - Selenium WebDriver errors: Confirm that ChromeDriver is updated and correctly configured.
- **Logging**: Errors and general output are logged to assist with debugging issues during execution.

## Contributing

Contributions to the project are welcome! Please fork the repository and submit a pull request with your proposed changes.
