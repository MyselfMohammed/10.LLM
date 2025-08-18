# Chat history display block

import streamlit as st

def render_chat_history(chat_history):
    """Render the user-bot chat history in Streamlit UI."""
    for sender, msg in chat_history:
        with st.chat_message("🧑" if sender == "user" else "🤖"):
            st.markdown(msg)
