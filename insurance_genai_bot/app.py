from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from ui.theme import setup_ui
from ui.greeting import show_greeting
from utils.session_state import init_session_state
from core.rag_engine import get_rag_chain
from core.chat_handler import handle_user_query
from ui.chat_history import show_chat_history

def main():
    setup_ui()
    init_session_state()

    # ---- Onboarding for user name ----
    if "username" not in st.session_state or not st.session_state.username:
        st.markdown(
            "<h1>🩺 Welcome to Medrisk Insurance Assistant</h1><h3>Please Enter Your Name:</h3>",
            unsafe_allow_html=True,
        )
        username = st.text_input("", key="input_name", label_visibility="collapsed")
        if username:
            st.session_state.username = username
            st.rerun()
        st.stop()

    show_greeting()
    qa_chain = get_rag_chain()

    # ---- Render chat history (as chat bubbles) ----
    show_chat_history(st.session_state.chat_history)

    # ---- Input bar at bottom, with session close ----
    handle_user_query(qa_chain)


if __name__ == "__main__":
    main()
