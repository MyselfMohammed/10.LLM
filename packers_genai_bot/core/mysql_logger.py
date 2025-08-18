# ---------------------- Logger ----------------------

import mysql.connector
import streamlit as st

MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "packers_chatbot"
}

def log_to_mysql(name, message):
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO chat_logs (customer_name, message) VALUES (%s, %s)", (name, message))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        st.error(f"MySQL Logging Error: {e}")
