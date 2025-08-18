# ---------------------- Session State Initialization ----------------------

import streamlit as st

def init_session_state():
    """Initializes default session state values."""
    defaults = {
        "name": "",
        "chat_history": [],
        "show_estimation_ui": False,
        "estimation_result": "",
        "estimation_done": False
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
