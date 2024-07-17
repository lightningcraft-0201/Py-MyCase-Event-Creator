import os
import json
import time
import base64
from datetime import datetime

from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from google_auth_oauthlib.flow import InstalledAppFlow

import dotenv

# Load environment variables
dotenv.load_dotenv()

# Google Sheets credentials JSON content
GOOGLE_SHEETS_CREDENTIALS = {
  "type": "service_account",
  "project_id": "devlopment-420411",
  "private_key_id": "0810a9a859e8ab76decbaf00624bf8864058b8a0",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC7yLwmFVHeLt30\nVLqFb+3ZFp0uDmfV1ZtpJtXLEGlR0cx1L13OVoSI1NVkJ2gJkO80ERRqqgQQKsVu\nnIqh09EDvWLRnbhYH9dJe1Jilvb8G+J4g5Uxf0z9KL6rjxJFs9Gm4z07vETQcqwz\na1E7kSeoUf9HKJ2qBRYIU3K1HLtU9qP6t7w/3wOupoVK/M1Y1Hm5lTRa7PXck0MJ\nSBAosvJGVkIn9PkUD5gg23BYl816PRB7w5ZXm+0nS23Q17MP4p7tZyqzZZ8e3Dh+\nBe9sxrii0wSQA6jqbsSLNh8Ts5b5yEGTPneC91RnENirZYCaVbxMIwywxr9/UEZr\nCMrjLw0VAgMBAAECggEAHN8i4HcYMIFDsnCBggkgyGcj8QQZfmTagWsNZWyHSONp\nHF5VPaeLNo+EpKKzaf8c7AQxP6oWuFafJt/OJ83tnbXVVvW5NWFl5CAgHVTpMf9m\njVFr06GnOGg2kqGLdWiNlCtti3zplqP+6mP2aCJr9sLurSXnQdAI4GxWH1cEzW3g\nAIMbx9t6UuyxZHz1RrR3vdpb3Rqk7d6pgs2bKzoA8hzzD22kTsYZ1fl02Q4loVJ+\njnUPfW72KZVF1/e5fpQ8GTh+FCBIiQQXp3c7GrC2211sBMXPdjBcsuFcAUUCamiN\nOFS1/CXETDx1gLvTAV4OQCfhJJal2YwZI9iZItabIQKBgQDeKLTZFKzngDVWQl7t\n3Rz/Cr6kmt/TKPrQX5gUeExmOoeoksCCFmO7Kisv4Fsk8je3LECDCmTBrrXE3/BW\nZiXr0Xh/NXF+LlbQPANr2dXt+1V9WG/WJJFWNA9VNIgoLMMSHK6dknVaOnZTAJsx\n3tnG/1gRYJhW15Sy+3Ch5WhDoQKBgQDYY4xfUt+wAQPo3P926CnfUmAzbLsxb9QK\nlj+oB8s1bUMGsXU7a/MZfF5veJLerEKBPn/hxBE6vTPHGtkIpkNpc3riySdC1Iuq\nY4/Nhv3WJ6oOPxu/T8zUs9hHnEmKeGsOEc8I+fi1YVwMYqjuKiIjPeoKJRqZjq1W\nWRJvREXU9QKBgERZW8KJ5ORYgpBmXRRreddRs/OqnoA11Gy1bHGnzUGKcmA/vjCH\nuOlFgQH60a/dQZz+ZV6rnPIl0VCf4S6DwNj7mknw5FkA4r6wKBFPdM0CDXxB8C5/\nE6Pk4m7Beb56fw2ce3CJNcerwumofxbpzDC4MJ0wDc5yBxLF3xJAJULhAoGBAJrS\nDtsdBmJ9N3jitf0zetIHtEDW6NAkPMgeXAkzGldth2lAiqorQFHZxA9pa1vaT/L8\n7q5vhAxM1sD8GpCvtMe8Eg408dxFCnCsr3TTwsX4txleWdH1nI4K5xHFZnCmW6JD\nZ6f6gdH0iNFrvYY5qxcf81Wy2mdHyAlhzWjCplwJAoGBAMxa0oevImOqMYOIqAen\nSwcyrGad3oPK0ywEG54H08tM1ZbKaWOekcGwzPx9iJKRqWck0+IyqxP/OSEhULX8\nEbMetToQTxNR9s1bvWSkoUjzdzk/JLdLx9sc0euKLTEDV00JJR/8wTZOBC9aCkXM\n80C1Tu3V07VYmoW/6AZR7K/H\n-----END PRIVATE KEY-----\n",
  "client_email": "elo-460@devlopment-420411.iam.gserviceaccount.com",
  "client_id": "100469084316918863490",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/elo-460%40devlopment-420411.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

# Gmail credentials JSON content
GMAIL_CREDENTIALS = {
    "installed": {
        "client_id": "97368303542-kbkqltk5ld8ktvorhnsf31gqvsno260g.apps.googleusercontent.com",
        "project_id": "casenet-424718",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "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",
        "redirect_uris": [
            "http://localhost"
        ]
    }
}

# Scopes define the level of access you need: readonly or full access
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Set the scope and credentials for Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(GOOGLE_SHEETS_CREDENTIALS, scope)
client = gspread.authorize(creds)

# Open the Google Spreadsheet by title
sheet_url = "https://docs.google.com/spreadsheets/d/1CTo6x7Hcn_KDR0Npt_6BR9NIz2L7vb76qgBayT-SlHg/edit?usp=sharing"
spreadsheet = client.open_by_url(sheet_url)

worksheet = spreadsheet.get_worksheet(0)

worksheet_name = "Sheet1"

# If the worksheet is not found, create a new one
if worksheet is None:
    worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows="100", cols="20")

# Define the header names
header_names = ["Subject", "Case Number", "Start Date", "Start Time", "Location", "Is Case Matched", "Is Event Created"]
existing_headers = worksheet.row_values(1)
if not existing_headers:
    worksheet.insert_row(header_names, index=1)

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
                flow = InstalledAppFlow.from_client_config(GMAIL_CREDENTIALS, SCOPES)
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

def list_messages(service, user_id='', label_ids=['CATEGORY_PERSONAL']):
    """Lists the IDs of all messages in the user's Primary category."""
    response = service.users().messages().list(userId=user_id).execute()
    messages = response.get('messages', [])
    return messages

def decode_part(part):
    """Decodes a single part of an email."""
    data = part['body'].get('data')
    if data:
        return base64.urlsafe_b64decode(data.encode('ASCII')).decode('utf-8')
    return ""

def extract_case_header(subject):
    # Find the last occurrence of the hyphen
    last_hyphen_index = subject.rfind('-')
    # Slice the string from the character after the hyphen to the end
    if last_hyphen_index != -1:
        return subject[last_hyphen_index + 1:].replace('ST V', '').strip()
    else:
        return subject  # Return the original string if there's no hyphen
    
def extract_case_number(subject):
    # Find the index of the first and last hyphen
    first_hyphen_index = subject.find('-')
    last_hyphen_index = subject.rfind('-')

    # Check if there are at least two hyphens and they are not the same
    if first_hyphen_index != -1 and last_hyphen_index != -1 and first_hyphen_index != last_hyphen_index:
        # Extract the substring between the first and last hyphen
        return subject[first_hyphen_index + 1:last_hyphen_index].strip()
    else:
        return ""  # Return an empty string if conditions aren't met  

def extract_scheduled_data(table):
    if table:
        # Iterate through all table rows
        for row in table.find_all('tr'):
            hearing_type = None
            # Check if 'Scheduled For' is in the row's text
            if 'Scheduled For' in row.get_text():
                # Find the element that contains 'Scheduled For'
                scheduled_for_element = row.find(string=lambda text: 'Scheduled For' in text)
                if scheduled_for_element:
                    # Find the next element in the HTML structure
                    prvious_element = row.find_previous('tr')
                    for td in prvious_element.find_all('td'):
                        if 'Scheduled' in td.text:
                            hearing_type = td.text.strip()
                            break
                    next_element = row.find_next('tr')
                    return [next_element.get_text().strip(), hearing_type] if next_element and prvious_element else None
    return None

def process_payload(payload, subject):
    """Recursively search for and return HTML content from the email payload."""
    if 'parts' in payload:  # Check if this is a multipart message
        for part in payload['parts']:
            html_content = process_payload(part, subject)
            if part.get('mimeType') == 'text/html' and html_content:
                soup = BeautifulSoup(html_content, 'html.parser')
                table = soup.find('table', style='font:sans-serif;border-collapse:collapse')
                hearing_data = extract_scheduled_data(table)
                if hearing_data != None:
                    hearing_time = hearing_data[0].split(';')[0].split('-')[0].strip()
                    hearing_type = hearing_data[1].replace(' Scheduled', '')
                    judge_name = hearing_data[0].split(';')[0].split('-')[1].strip().split(" ")[-1]
                else:
                    hearing_time = ''
                    hearing_type = ''
                    judge_name = ''
                subject.split(',')
                county = subject.split(',')[1].replace(' - ', ' ').strip()
                defendant_first_name = extract_case_header(subject.split(',')[0]).split(" ")[0]
                defendant_last_name = extract_case_header(subject.split(',')[0]).split(" ")[-1]
                case_number = extract_case_number(subject.split(',')[0])
                lawyer_name = 'Andrew T Morris' if 'TO: Andrew T Morris'.lower() in soup.text.lower() else 'David Christopher LaPee' if 'TO: David Christopher LaPee'.lower() in soup.text.lower() else 'None'                

                # Format the date with slashes
                if hearing_time != '':
                    dt = datetime.strptime(hearing_time, "%m/%d/%y %I:%M %p")
                    # Extract the date and time
                    court_date = dt.date().strftime("%m/%d/%Y")  # Gets the date part formatted as 'mm/dd/yyyy'
                    court_time = dt.time().strftime("%I:%M %p")  # Gets the time part
                    event_name = f'{defendant_last_name}, {defendant_first_name} St v--{county}--{judge_name}--{hearing_type}'
                    print([case_number, event_name, court_date, court_time, county])
                    
                    create_event(case_number, event_name, court_date, court_time, county, subject)
    elif payload.get('mimeType') == 'text/html':
        content = decode_part(payload)
        if content:
            return content
        else:
            print("Debug: Found HTML MIME type but no content.")
    return ""  # Return an empty string if no HTML content is found

def get_message(service, msg_id, user_id='me'):
    """Fetches and processes a single message by ID, printing HTML content if available."""
    message = service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
    
    headers = message['payload']['headers']
    subject = next((header['value'] for header in headers if header['name'] == 'Subject'), "")
    print(subject)
    if 'eNotice' in subject:
        process_payload(message['payload'], subject)

def create_message(to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()
    return {'raw': raw}

def get_new_messages(service, saved_ids):
    # Get all messages from the service
    all_messages = list_messages(service)
    # Filter messages that are not in the saved IDs array
    new_messages = [msg for msg in all_messages if msg['id'] not in saved_ids]
    
    return new_messages

def read_saved_ids(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data.get("saved_ids", [])
    except FileNotFoundError:
        return []

def write_saved_ids(filename, saved_ids):
    with open(filename, 'w') as file:
        json.dump({"saved_ids": saved_ids}, file, indent=4)

def create_event(case_number, event_name, start_date, start_time, location, subject):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Ensure GUI is off
    chrome_options.add_argument("--window-size=1920,1080")  # Set a window size
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Load environment variables
    dotenv.load_dotenv()

    # Environment variables for AWS
    USER_NAME = os.getenv("USER_NAME", "")
    USER_PASS = os.getenv("USER_PASS", "")
    driver.get('https://www.mycase.com/login/')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login_session_email')))
    username_field = driver.find_element(By.ID, 'login_session_email')
    password_field = driver.find_element(By.ID, 'login_session_password')
    submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')

    username_field.send_keys(USER_NAME)
    password_field.send_keys(USER_PASS)
    submit_button.click()

    # Wait for the element <span class="modal-title">Upcoming Reminders</span>
    try:
        upcoming_reminders = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.modal-title"))
        )
        if upcoming_reminders.text == "Upcoming Reminders":
            # Find the div element by its ID within the button
            cancel_button = driver.find_element(By.CSS_SELECTOR, "button.cancel-button.btn-link.btn.btn-link")
            cancel_button.click()

    except TimeoutException:
        print("The element 'Upcoming Reminders' was not found.")
    time.sleep(1)
    # After submitting the login form
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".dashboard-add-item-section.d-flex"))
    )

    element = driver.find_element(By.CSS_SELECTOR, ".dashboard-event.test-add-event.pendo-add-event.pendo-exp2-add-event")
    element.click()

    time.sleep(1)

    # Find the div element by its ID within the button
    case_element = driver.find_element(By.CSS_SELECTOR, ".row.g-0")

    # Click on the div element
    case_element.click()

    time.sleep(1)

    # Find the input element by the aria-activedescendant attribute
    input_case = driver.find_element(By.CSS_SELECTOR, 'input[aria-activedescendant="react-select-2--option-0"]')

    # Input the desired value into the element
    input_case.send_keys(case_number)
    time.sleep(1.5)
    if "results" in driver.find_element(By.CSS_SELECTOR, ".Select-menu-outer").text:
        record = [subject, case_number, start_date, start_time, location, "𝑵𝒐", "𝑵𝒐"]
        worksheet.append_row(record)
        return print("No case found")
    # Press the Enter key
    input_case.send_keys(Keys.ENTER)

    # Find the input element by its ID
    input_name = driver.find_element(By.ID, "name")

    # Clear any pre-existing text in the input field
    input_name.clear()

    # Input the desired value into the element
    input_name.send_keys(event_name)

    # Find the div element by its ID within the button
    color_element = driver.find_element(By.ID, "chosen-category")

    # Click on the div element
    color_element.click()

    # Find the div element by its ID
    color_item = driver.find_element(By.ID, "item_category_2085055")

    # Click on the div element
    color_item.click()

    # Find the input element by its ID
    input_start_date = driver.find_element(By.ID, "appointment_rule_start_date")

    # Clear any pre-existing text in the input field
    input_start_date.clear()

    # Input the desired value into the element
    input_start_date.send_keys(start_date)

    # Press the Enter key
    input_start_date.send_keys(Keys.ENTER)

    # Find the input element by its ID
    input_start_time = driver.find_element(By.ID, "appointment_rule_start_time")

    # Clear any pre-existing text in the input field
    input_start_time.clear()

    # Input the desired value into the element
    input_start_time.send_keys(start_time)

    # Press the Enter key
    input_start_time.send_keys(Keys.ENTER)

       # Find the div element by its ID within the button
    location_element = driver.find_element(By.CSS_SELECTOR, ".col-sm-8")

    # Click on the div element
    location_element.click()

    time.sleep(1)

    # Find the input element by the aria-activedescendant attribute
    input_location = driver.find_element(By.CSS_SELECTOR, 'input[aria-activedescendant="react-select-3--option-0"]')

    # Input the desired value into the element
    input_location.send_keys(location)
    time.sleep(1.5)
    # Press the Enter key
    input_location.send_keys(Keys.ENTER)

    # Find the input element by its ID
    input_description = driver.find_element(By.ID, "description")

    # Clear any pre-existing text in the input field
    input_description.clear()

    # Input the desired value into the element
    input_description.send_keys("Event Description")

    if driver.find_element(By.NAME, "client-share-all"):
        # Find the checkbox by its name attribute
        checkbox_share = driver.find_element(By.NAME, "client-share-all")

        # Click on the checkbox
        checkbox_share.click()

    if driver.find_element(By.NAME, "client-attend-all"):
        # Find the checkbox by its name attribute
        checkbox_attend = driver.find_element(By.NAME, "client-attend-all")

        # Click on the checkbox
        checkbox_attend.click()

    create_button = driver.find_element(By.CSS_SELECTOR, ".btn.btn-cta-primary")
    create_button.click()
    record = [subject, case_number, start_date, start_time, location, "𝐘𝐞𝐬", "𝐘𝐞𝐬"]
    worksheet.append_row(record)

    time.sleep(2) 
    driver.quit()

def main():
    while True:
        try:
            service = authenticate_gmail()
            filename = 'saved_ids.json'
            
            # Read saved IDs from the JSON file
            saved_ids = read_saved_ids(filename)
            
            # Get new messages
            new_messages = get_new_messages(service, saved_ids)
            
            if new_messages:
                for message in new_messages:  # Limit to first 5 messages for demonstration
                    get_message(service, message['id'])
                    
                    # Update saved_ids with the current message ID
                    saved_ids.append(message['id'])
                    
                    # Write updated saved_ids back to file after each message is processed
                    write_saved_ids(filename, saved_ids)

                    # Print updated saved_ids
                    print("Updated saved_ids:", saved_ids)
            else:
                print("No new messages to process")
            time.sleep(5)
        except Exception as e:
            print(f'Error: {e}')

if __name__ == "__main__":
    main()
