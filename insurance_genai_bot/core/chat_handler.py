import streamlit as st
from core.user_input_validation import validate_user_query

def handle_user_query(qa_chain):
    # Session control: Only show input if not closed
    if "chat_active" not in st.session_state:
        st.session_state.chat_active = True
    if not st.session_state.chat_active:
        st.warning("🔒 Session closed. Please refresh the page to start again.")
        return

    with st.form(key="user_input_form", clear_on_submit=True):
        user_query = st.text_input(
            "Type your message...", key="user_input", label_visibility="collapsed"
        )
        submit = st.form_submit_button("Send")

    if submit and user_query.strip():
        # Check for exit/close/quit
        if user_query.strip().lower() in ["exit", "close", "quit"]:
            st.session_state.chat_active = False
            st.session_state.chat_history.append(
                ("assistant", "🔒 Session closed. Thank you!")
            )
            st.rerun()
        # Validate input
        is_valid, message = validate_user_query(user_query)
        if not is_valid:
            st.error(message)
            return
        # Append user message
        st.session_state.chat_history.append(("user", user_query.strip()))
        with st.spinner("Thinking..."):
            response = qa_chain.invoke(user_query)
            answer = response["result"].strip()
            # Major QA: Only append if valid, else warn
            if not answer or len(answer) < 10:
                st.session_state.chat_history.append(
                    (
                        "assistant",
                        "Sorry, no relevant answer found. Please ask another question.",
                    )
                )
            else:
                st.session_state.chat_history.append(("assistant", answer))
        st.rerun()
