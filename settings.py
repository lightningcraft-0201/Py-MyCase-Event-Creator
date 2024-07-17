import os
import dotenv

dotenv.load_dotenv()

# Google Sheets and Gmail credentials JSON content
GOOGLE_SHEETS_CREDENTIALS_PATH = os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH')
CREDENTIALS_PATH = os.getenv('CREDENTIALS_PATH')

# Scopes define the level of access you need: readonly or full access
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
SHEET_SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
SHEET_URL = "https://docs.google.com/spreadsheets/d/1CTo6x7Hcn_KDR0Npt_6BR9NIz2L7vb76qgBayT-SlHg/edit?usp=sharing"
