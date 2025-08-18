
# ---------------------- Chat Input Processing ----------------------

from core.safety_check import is_safe_input
from core.mysql_logger import log_to_mysql

def process_user_query(query, qa_chain):
    """
    Processes the incoming query:
    - Checks for moderation
    - Adds to chat history
    - Routes to estimation or RAG
    - Logs messages
    """
    import streamlit as st

    if not is_safe_input(query):
        st.warning("⚠️ Kindly rephrase your sentence properly to proceed further.")
        return

    user_msg = f"{st.session_state.name}: {query}"
    st.session_state.chat_history.append(("user", user_msg))
    log_to_mysql(st.session_state.name, query)

    if any(k in query.lower() for k in ["estimate", "estimation", "calculate", "cost", "price"]):
        st.session_state.show_estimation_ui = True
        bot_msg = "Sure! Please fill in the details below to get your estimation. 👇"
    else:
        bot_msg = qa_chain.run(query)

    st.session_state.chat_history.append(("bot", f"i-Assist: {bot_msg}"))
    log_to_mysql("bot", bot_msg)
