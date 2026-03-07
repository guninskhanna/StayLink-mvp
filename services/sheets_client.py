import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import streamlit as st
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["google"],
    scopes=scope
)



client = gspread.authorize(creds)
drive_service = build("drive", "v3", credentials=creds)
sheet = client.open("StayLink_QBS_MVP")

transactions = sheet.worksheet("Transactions")


def log_transaction(token, guest_name, room, merchant_name, amount, receipt_link, merchant_pin):
    transaction_id = generate_transaction_id()
    timestamp = datetime.utcnow().isoformat()

    transactions.append_row([
        transaction_id,   # transaction_id
        timestamp,        # timestamp
        token,            # token
        guest_name,       # guest_name
        room,             # room
        merchant_name,    # merchant
        amount,           # amount
        receipt_link,     # recipet_link
        merchant_pin      # merchant_pin
    ])

def validate_merchant(pin):

    merchants = sheet.worksheet("Merchants")

    records = merchants.get_all_records()

    for merchant in records:
        if str(merchant["pin"]) == str(pin):

            if merchant["active_status"] == "ACTIVE":
                return True, merchant["merchant_name"]

            else:
                return False, "Merchant inactive"

    return False, "Invalid PIN"

def validate_guest(token):
    guests = sheet.worksheet("Guests")
    records = guests.get_all_records()

    for guest in records:
        if str(guest["token"]) == str(token):
            if guest["status"] == "ACTIVE":
                return True, {
                    "guest_name": guest["guest_name"],
                    "room": guest["room"]
                }
            else:
                return False, "Guest stay inactive"

    return False, "Invalid guest token"

def generate_transaction_id():
    records = transactions.get_all_records()
    next_num = len(records) + 1
    return f"TXN-{next_num:06d}"

def upload_receipt(file, filename):

    folder_id = "15vTs0Lgqk8EYRfJ4-Tu8WgzZN4IzBXbl"

    file_stream = io.BytesIO(file.read())

    media = MediaIoBaseUpload(
        file_stream,
        mimetype=file.type,
        resumable=False
    )

    metadata = {
        "name": filename,
        "parents": [folder_id]
    }

    uploaded = drive_service.files().create(
        body=metadata,
        media_body=media,
        fields="id",
        supportsAllDrives=True
    ).execute()

    file_id = uploaded.get("id")

    return f"https://drive.google.com/file/d/{file_id}/view"