import schedule
import time
from google_auth import authenticate_gmail
from email_processing import list_messages, get_message, process_payload, get_new_messages
from utils import read_saved_ids, write_saved_ids

def main():
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
            print("Updated saved_ids")
    else:
        print("No new messages to process")

schedule.every().day.at("04:00").do(main)
main()

while True:
    schedule.run_pending()
    time.sleep(1)
