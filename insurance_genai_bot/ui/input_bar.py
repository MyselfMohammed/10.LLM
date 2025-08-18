import streamlit as st
from core.chat_logic import medrisk_bot_reply


def chat_input_bar():
    if st.session_state.chat_active:
        with st.form(key="user_input_form"):
            user_input = st.text_input(
                "Message", key="user_input", label_visibility="collapsed"
            )
            submit = st.form_submit_button("Send")
        if submit and user_input.strip():
            if user_input.strip().lower() in ["exit", "close", "quit"]:
                st.session_state.chat_active = False
                st.session_state.chat_history.append(
                    ("assistant", "🔒 Session closed. Thank you!")
                )
                st.experimental_rerun()
            else:
                st.session_state.chat_history.append(("user", user_input.strip()))
                bot_reply = medrisk_bot_reply(user_input.strip())
                st.session_state.chat_history.append(("assistant", bot_reply))
                st.experimental_rerun()
    else:
        st.warning("🔒 Session closed. Please refresh the page to start again.")
