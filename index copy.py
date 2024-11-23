import os
from flask import Flask, request, jsonify
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import google.auth

app = Flask(__name__)

# Google Sheets setup function
def get_google_sheets_service(credentials_path):
    creds, project = google.auth.load_credentials_from_file(credentials_path)
    service = build('sheets', 'v4', credentials=creds)
    return service

# Function to append data to Google Sheets
def append_google_sheet(spreadsheet_id, range_name, values, credentials_path):
    service = get_google_sheets_service(credentials_path)
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

# @app.route('/send_to_sheet', methods=['POST'])
# def send_to_sheet():
#     data = request.get_json()  # Get the JSON data from the request body
    
#     # Check if all required fields are present in the data
#     required_fields = ["Name", "Gender", "DOB", "Address", "CCCD", "CMND", "IssueDate"]
#     if not all(field in data for field in required_fields):
#         return jsonify({"error": "Missing required fields"}), 400

#     # Prepare the data to be inserted into Google Sheets
#     values = [[
#         "", 
#         data["Name"],
#         "", 
#         "", 
#         "", 
#         data["Gender"],
#         data["DOB"],
#         "", 
#         "", 
#         "", 
#         data["Address"],
#         data["CCCD"],
#         data["CMND"],
#         data["IssueDate"]
#     ]]

#     # Send data to Google Sheets
#     credentials_path = '/Users/mac/Documents/dowithqr/backend_py/key.json'  # Replace with your credentials path
#     spreadsheet_id = '1wX2cd9b-XM8e7PBCRa6wwbjMHk3iLBCoWHAw4hSP3ZE'  # Replace with your Google Sheets ID
#     range_name = 'Sheet1!A1'  # The range where the data will be appended (starting from A1)
    
#     append_google_sheet(spreadsheet_id, range_name, values, credentials_path)

#     return jsonify(data), 200

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
