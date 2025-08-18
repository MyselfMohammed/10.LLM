import streamlit as st


def init_session_state():
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "chat_active" not in st.session_state:
        st.session_state.chat_active = True
