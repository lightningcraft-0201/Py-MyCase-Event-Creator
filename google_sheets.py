from google_auth import authenticate_sheets

def update_sheet(data):
    worksheet = authenticate_sheets()
    worksheet.append_row(data)
