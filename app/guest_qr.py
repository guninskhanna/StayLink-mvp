import streamlit as st
import qrcode
from io import BytesIO

st.set_page_config(page_title="StayLink Guest QR")

st.title("Guest Charge QR")

# Read token from URL
token = st.query_params.get("token")

if not token:
    st.error("Invalid guest link.")
    st.stop()

merchant_url = f"http://localhost:8501/merchant?token={token}"

qr = qrcode.make(merchant_url)

buffer = BytesIO()
qr.save(buffer, format="PNG")

st.image(buffer.getvalue(), caption="Show this QR code to the merchant", width=450)


st.info("The merchant will scan this QR code to charge your purchase to your room.")