# ---------------------- Streamlit UI Config ----------------------

import streamlit as st

def setup_ui():
    """Sets Streamlit page config and applies global styles."""
    st.set_page_config("i-Assist Chatbot", layout="centered")
    
    st.markdown("""
    <style>
    .main {
        background-color: #fff9f5;
        padding-bottom: 5rem;
    }
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 2rem;
        left: 2rem;
        right: 2rem;
        background: white;
        box-shadow: 0px -2px 10px rgba(0,0,0,0.1);
        padding: 1rem;
        border-radius: 12px;
    }
    </style>
    """, unsafe_allow_html=True)
