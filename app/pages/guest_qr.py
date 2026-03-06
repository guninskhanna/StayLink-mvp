import streamlit as st
import qrcode
from io import BytesIO
from services.sheets_client import validate_guest

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
    st.error("Invalid access link.")
    st.stop()

valid, guest_result = validate_guest(token)

if not valid:
    st.error("This guest link is no longer active.")
    st.stop()

guest_name = guest_result["guest_name"]
room = guest_result["room"]

st.title("StayLink")
st.caption(f"Guest: {guest_name} | Room: {room}")

merchant_url = f"https://staylink-mvp.streamlit.app/merchant_form?token={token}"

qr = qrcode.make(merchant_url)

buffer = BytesIO()
qr.save(buffer, format="PNG")

col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.image(buffer.getvalue(), use_container_width=True)

st.markdown(
    """
    <div style="text-align:center; margin-top:20px;">
    Show this QR code to the merchant to charge purchases to your room.
    </div>
    """,
    unsafe_allow_html=True
)

st.caption("Valid for the duration of your stay.")
st.info("Show this QR code to the merchant to charge purchases to your room.")