import streamlit as st


def init_session_state():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
