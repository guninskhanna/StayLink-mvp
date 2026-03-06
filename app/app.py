import streamlit as st

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

st.set_page_config(page_title="StayLink")

st.title("StayLink")
st.write("Internal system")