import streamlit as st


def show_chat_history():
    st.markdown(
        "<style>.chat-bubble-user{background:#f0f5ff;border-radius:20px;padding:12px;margin-bottom:8px;max-width:60%;align-self:flex-end;}.chat-bubble-bot{background:#e6ffe6;border-radius:20px;padding:12px;margin-bottom:8px;max-width:60%;align-self:flex-start;}</style>",
        unsafe_allow_html=True,
    )
    for role, msg in st.session_state.chat_history:
        if role == "user":
            st.markdown(
                f'<div class="chat-bubble-user"><b>{
                    st.session_state.username}:</b> {msg}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="chat-bubble-bot"><b>🩺 Medrisk Assistant:</b> {msg}</div>',
                unsafe_allow_html=True,
            )
