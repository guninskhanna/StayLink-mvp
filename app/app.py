import streamlit as st

st.set_page_config(layout="centered")

hide_streamlit_style = """
<style>
[data-testid="stSidebar"] {display: none;}
[data-testid="collapsedControl"] {display: none;}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.set_page_config(page_title="StayLink")

st.title("StayLink")
st.write("Internal system")