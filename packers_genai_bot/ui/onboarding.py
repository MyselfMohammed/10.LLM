# ---------------------- Greeting + Name Input ----------------------

import streamlit as st
import time
from ui.greeting import get_ist_greeting

def handle_user_onboarding():
    """Handles greeting, name input, and greeting message."""
    
    # Show welcome header
    st.markdown(
        "<h3 style='text-align: center; font-size: 40px;'>🧳Welcome to Packers and Movers <br>(Powered by i-Assist)</h3>",
        unsafe_allow_html=True
    )

    # If name is not provided yet
    if not st.session_state.name:
        st.markdown(
            f"<h4 style='text-align: center; font-size: 40px;'>{get_ist_greeting()}! Please Enter Your Name 😊</h4>",
            unsafe_allow_html=True
        )
        name_input = st.chat_input("Type your name here...")

        if name_input:
            st.session_state.name = name_input
            time.sleep(0.5)
            st.rerun()
        else:
            st.stop()  # Wait here until name is entered

    # Show welcome message
    st.markdown(
    f"""
    <h3 style='text-align: center; font-size: 36px; font-weight: bold; color: green; background-color: #eafbe7; padding: 10px; border-radius: 10px;'>
        Welcome, {st.session_state.name}😃!!
    </h3>
    """,
    unsafe_allow_html=True)

    # Add bot's initial message (only once)
    if len(st.session_state.chat_history) == 0:
        st.session_state.chat_history.append(("bot", "How may I assist you today?"))

    # Return input box content
    return st.chat_input("Type your message...")
