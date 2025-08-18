# ---------------------- Standard Libraries ----------------------
import os
import re
import time

# ---------------------- Third-Party Libraries ----------------------
import streamlit as st
import mysql.connector
from dotenv import load_dotenv
import openai
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

# ---------------------- Internal Modules ----------------------
# Config
from config.env import OPENAI_API_KEY, MYSQL_CONFIG, FAISS_DB_PATH

# Core Logic
from core.safety_check import is_safe_input
from core.mysql_logger import log_to_mysql
from core.estimation import get_estimation_from_mysql
from core.pdf_generator import generate_pdf
from core.message_handler import process_user_query

# RAG Engine
from rag.chain import get_rag_chain

# UI Components
from ui.theme import setup_ui
from ui.greeting import get_ist_greeting
from ui.onboarding import handle_user_onboarding
from ui.forms import render_estimation_form, render_estimation_result
from ui.chat_display import render_chat_history

# Utilities
from utils.helpers import strip_unicode
from utils.session_state import init_session_state


# ---------------------- App Initialization ----------------------
def main():
    # 1️⃣ Setup UI theme (CSS, layout)
    setup_ui()

    # 2️⃣ Initialize session variables before using them
    init_session_state()

    # 3️⃣ Load your FAISS + LangChain RAG chain
    qa_chain = get_rag_chain()

    # 4️⃣ Handle onboarding – name input, greeting, and get query
    query = handle_user_onboarding()

    # 5️⃣ Process the query (RAG or estimation decision)
    if query:
        process_user_query(query, qa_chain)

    # 6️⃣ Show estimation form or result
    if st.session_state.get("show_estimation_ui", False):
        if not st.session_state.get("estimation_done", False):
            render_estimation_form()
        else:
            render_estimation_result()

    # 7️⃣ Finally render the chat history
    render_chat_history(st.session_state.chat_history)

# ---------------------- Entry Point ----------------------
if __name__ == "__main__":
    main()
