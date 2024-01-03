import time

import streamlit as st
from dotenv import load_dotenv
# from PIL import Image

load_dotenv()


def initialize():
    if "login_id" not in st.session_state:
        st.session_state.login_id = "AnonymousUser"


def change_user():
    if 'messages' in st.session_state:
        del st.session_state.messages


st.set_page_config(page_title="My Dentist")

st.title("My Dentist")
values = ['AnonymousUser', 'AndrewNg', 'ElonMusk', 'AntonA']
st.session_state.login_id = st.selectbox('Please let me know who you are.', values, index=0 if 'login_id' not in st.session_state else values.index(st.session_state.login_id), on_change=change_user)

initialize()

# hide_svalues <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)
