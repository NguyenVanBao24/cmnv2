import os
from flask import Flask, request, jsonify
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import google.auth
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

app = Flask(__name__)
load_dotenv()  # Load các biến môi trường từ file .env

# Lấy các giá trị từ biến môi trường
GOOGLE_SHEET_SPREADSHEET_ID = os.getenv('GOOGLE_SHEET_SPREADSHEET_ID')
GOOGLE_PROJECT_ID = os.getenv('GOOGLE_PROJECT_ID')
GOOGLE_PRIVATE_KEY = os.getenv('GOOGLE_PRIVATE_KEY').replace("\\n", "\n")
GOOGLE_CLIENT_EMAIL = os.getenv('GOOGLE_CLIENT_EMAIL')

def get_google_sheets_service():
    # Tạo credentials từ các biến môi trường
    credentials_info = {
        "type": "service_account",
        "project_id": GOOGLE_PROJECT_ID,
        "private_key_id": os.getenv('GOOGLE_PRIVATE_KEY_ID'),
        "private_key": GOOGLE_PRIVATE_KEY,
        "client_email": GOOGLE_CLIENT_EMAIL,
        "client_id": os.getenv('GOOGLE_CLIENT_ID'),
        "auth_uri": os.getenv('GOOGLE_AUTH_URI'),
        "token_uri": os.getenv('GOOGLE_TOKEN_URI'),
        "auth_provider_x509_cert_url": os.getenv('GOOGLE_AUTH_PROVIDER_X509_CERT_URL'),
        "client_x509_cert_url": os.getenv('GOOGLE_CLIENT_X509_CERT_URL'),
        "universe_domain": os.getenv('GOOGLE_UNIVERSE_DOMAIN')
    }

    creds = Credentials.from_service_account_info(credentials_info)
    service = build('sheets', 'v4', credentials=creds)
    return service

# Function to append data to Google Sheets
def append_google_sheet(spreadsheet_id, range_name, values):
    service = get_google_sheets_service()
    body = {'values': values}
    try:
        # Append data to the next available row
        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",  # Insert new rows at the next available spot
            body=body
        ).execute()
        print(f"{result.get('updates').get('updatedCells')} cells updated.")
    except HttpError as err:
        print(f"Error: {err}")

@app.route('/send_to_sheet', methods=['POST'])
def send_to_sheet():
    data = request.get_json()  # Get the JSON data from the request body
    
    # Check if all required fields are present in the data
    required_fields = ["Name", "Gender", "DOB", "Address", "CCCD", "CMND", "IssueDate"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    # Prepare the data to be inserted into Google Sheets
    values = [[
        "", 
        data["Name"],
        "", 
        "", 
        "", 
        data["Gender"],
        data["DOB"],
        "", 
        "", 
        "", 
        data["Address"],
        data["CCCD"],
        data["CMND"],
        data["IssueDate"]
    ]]

    # Send data to Google Sheets
    append_google_sheet(GOOGLE_SHEET_SPREADSHEET_ID, 'Sheet1!A1', values)

    return jsonify(data), 200

@app.route('/', methods=['GET'])
def test():
    return jsonify([
        {
            "CCCD": "0485 0000 0541",
            "CMND": "201 807 254",
            "Name": "Nguyễn Phan Niên Thảo",
            "Gender": "Nữ",
            "DOB": "06/06/2000",
            "Address": "Tổ 79, Thọ Quang, Sơn Trà, Đà Nẵng",
            "Issue Date": "22/04/2021"
        }
    ])

if __name__ == '__main__':
    app.run(debug=True)
