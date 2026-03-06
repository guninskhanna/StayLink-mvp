import sys
import os
from datetime import datetime

st.set_page_config(layout="centered")

hide_streamlit_style = """
<style>

/* Hide hamburger menu */
#MainMenu {visibility: hidden;}

/* Hide footer */
footer {visibility: hidden;}

/* Hide header */
header {visibility: hidden;}

/* Hide top-right toolbar */
[data-testid="stToolbar"] {display: none;}

/* Hide Streamlit deploy button */
[data-testid="stDecoration"] {display: none;}

/* Hide bottom-right manage app button */
[data-testid="stStatusWidget"] {display: none;}

</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
from services.sheets_client import log_transaction, validate_merchant, validate_guest

st.set_page_config(page_title="StayLink Merchant")

st.title("Charge to Room")

# Read token from QR URL
token = st.query_params.get("token")
st.info(f"Charging guest token: {token}")

if not token:
    st.error("Invalid QR code.")
    st.stop()

st.success("Guest verified")

st.write("Enter charge details")

# Merchant inputs
pin = st.text_input("Merchant PIN", type="password")
amount = st.number_input("Bill Amount", min_value=0.0, step=1.0)
receipt = st.file_uploader(
    "Upload receipt photo (optional)",
    type=["png", "jpg", "jpeg"]
)

receipt_link = ""
if receipt:
    os.makedirs("receipts", exist_ok=True)
    filename = f"receipts/{datetime.utcnow().timestamp()}_{receipt.name}"
    with open(filename, "wb") as f:
        f.write(receipt.getbuffer())
    receipt_link = filename

submit = st.button("Submit Charge")

if submit:

    valid_guest, guest_result = validate_guest(token)
    if not valid_guest:
        st.error(guest_result)
        st.stop()

    guest_name = guest_result["guest_name"]
    room = guest_result["room"]

    valid_merchant, merchant_result = validate_merchant(pin)
    if not valid_merchant:
        st.error(merchant_result)
        st.stop()

    merchant_name = merchant_result

    receipt_link = filename if receipt else ""

    log_transaction(
        token=token,
        guest_name=guest_name,
        room=room,
        merchant_name=merchant_name,
        amount=amount,
        receipt_link=receipt_link,
        merchant_pin=pin
    )

    st.success("Charge recorded successfully")
    st.balloons()