import streamlit as st
import qrcode
from io import BytesIO

st.set_page_config(layout="centered")

hide_streamlit_style = """
<style>
[data-testid="stSidebar"] {display: none;}
[data-testid="collapsedControl"] {display: none;}

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