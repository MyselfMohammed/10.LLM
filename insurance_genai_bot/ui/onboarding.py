import streamlit as st


def onboarding_screen():
    st.markdown(
        "<h1>🩺 Welcome to Medrisk Insurance Assistant</h1><h3>Please Enter Your Name:</h3>",
        unsafe_allow_html=True,
    )
    username = st.text_input("Name", key="input_name", label_visibility="collapsed")
    if username:
        st.session_state.username = username
        st.st.rerun()
    st.stop()
