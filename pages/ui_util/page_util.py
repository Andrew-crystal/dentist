import os
from time import sleep

import streamlit as st
from auth0_component import login_button


#clientId = os.getenv("AUTH0_CLIENT_ID")
#domain = "eagertest.us.auth0.com"


# def check_client_login():
#     if not clientId:
#         raise Exception("AUTH0_CLIENT_ID not set.")
#     user_info = login_button(clientId, domain=domain, key="AuthButton")
#     if user_info:
#         # just for debug
#         print(user_info)
#
#         st.session_state["email"] = user_info.get("email")
#         st.session_state["token"] = user_info.get("token")
#         st.rerun()


# def show_user_header():
#     if not st.session_state.get("token"):
#         check_client_login()
#     else:
#         st.write(f"Wellcome: {st.session_state.email}")
#         if st.button("Logout"):
#             del st.session_state["token"]
#             del st.session_state["email"]
#             st.rerun()


class PageUtil:
    @staticmethod
    def waiting_for_input(is_question: bool):
        w = "next question" if is_question else "both answers"
        st.info(f"waiting for **{w}** ...")
        if st.button("Refresh to check again"):
            with st.spinner():
                sleep(2)
                st.rerun()
