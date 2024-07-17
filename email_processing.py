import base64
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from google_auth import authenticate_gmail
from webdriver_utils import create_event
from email.mime.text import MIMEText

def list_messages(service, user_id='me', label_ids=['INBOX']):
    """Retrieve a list of all messages in the user's mailbox."""
    try:
        all_messages = []
        request = service.users().messages().list(userId=user_id, labelIds=label_ids)
        
        while request:
            response = request.execute()
            messages = response.get('messages', [])
            all_messages.extend(messages)
            request = service.users().messages().list_next(request, response)
        
        return all_messages
    except Exception as e:
        print(f"Failed to retrieve messages: {e}")
        return []

def get_message(service, msg_id, user_id='me'):
    try:
        """Fetches and processes a single message by ID, printing HTML content if available."""
        message = service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
        
        headers = message['payload']['headers']
        subject = next((header['value'] for header in headers if header['name'] == 'Subject'), "")
        print(subject)
        # Extract the received date from internalDate
        
        received_timestamp = int(message['internalDate']) / 1000  # Convert milliseconds to seconds
        received_date = datetime.fromtimestamp(received_timestamp).strftime('%m/%d/%Y')  # Formatting date as 'MM/DD/YYYY'
        
        if 'eNotice' in subject:
            process_payload(message['payload'], subject, msg_id, received_date)
    except Exception as e:
        print(f'Error: {e}')
        time.sleep(10)
        get_message(service, msg_id, user_id='me')

def decode_part(part):
    """Decodes a single part of an email."""
    data = part['body'].get('data')
    if data:
        return base64.urlsafe_b64decode(data.encode('ASCII')).decode('utf-8')
    return ""

def create_message(to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()
    return {'raw': raw}

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
                        if 'Sched' in td.text:
                            hearing_type = td.text.strip()
                            break
                    next_element = row.find_next('tr')
                    return [next_element.get_text().strip(), hearing_type] if next_element and prvious_element else None
    return None

def process_payload(payload, subject, msg_id, received_date):
    """Recursively search for and return HTML content from the email payload."""
    if 'parts' in payload:  # Check if this is a multipart message
        for part in payload['parts']:
            html_content = process_payload(part, subject, msg_id, received_date)
            if part.get('mimeType') == 'text/html' and html_content:
                soup = BeautifulSoup(html_content, 'html.parser')
                table = soup.find('table', style='font:sans-serif;border-collapse:collapse')
                hearing_data = extract_scheduled_data(table)
                if hearing_data != None:
                    hearing_time = hearing_data[0].split(';')[0].split('-')[0].strip()
                    if " Sched" not in hearing_data[1]:
                        hearing_type = 'Initial Appearance'
                    else:
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
                    
                    create_event(case_number, event_name, court_date, court_time, hearing_type, county, subject, msg_id, received_date)
    elif payload.get('mimeType') == 'text/html':
        content = decode_part(payload)
        if content:
            return content
        else:
            print("Debug: Found HTML MIME type but no content.")
    return ""  # Return an empty string if no HTML content is found

def get_new_messages(service, saved_ids):
    # Get all messages from the service
    all_messages = list_messages(service)
    # Filter messages that are not in the saved IDs array
    new_messages = [msg for msg in all_messages if msg['id'] not in saved_ids]
    
    return new_messages
