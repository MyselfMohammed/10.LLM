# ---------------------- Standard Libraries ----------------------
import os
import re

# ---------------------- Third-Party Libraries ----------------------
import streamlit as st
import mysql.connector
from dotenv import load_dotenv
import openai

# ---------------------- LangChain Modules ----------------------
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

# ---------------------- Custom Utilities ----------------------
from utils import (
    get_ist_greeting,
    is_safe_input,
    log_to_mysql,
    get_estimation_from_mysql,
    strip_unicode,
    generate_pdf
)

# ---------------------- Environment Setup ----------------------
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# ---------------------- MySQL Config ----------------------
MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "packers_chatbot"
}

# ---------------------- FAISS + LangChain Setup ----------------------
vectorstore = FAISS.load_local(
    "vectordb/packers_faiss",
    OpenAIEmbeddings(),
    allow_dangerous_deserialization=True
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
llm = ChatOpenAI(temperature=0.3)
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type="stuff")

# ---------------------- Streamlit UI Config ----------------------
st.set_page_config("i-Assist Chatbot", layout="centered")
st.markdown("""
    <style>
    .main { background-color: #fff9f5; }
    div[data-testid="stChatInput"] { position: fixed; bottom: 0; width: 100%; background: white; }
    </style>
""", unsafe_allow_html=True)

# ---------------------- UI: Greeting & Name Input ----------------------
st.title("💬 i-Assist of Packers and Movers (Powered by Hope-AI) 🧳")

if "name" not in st.session_state:
    st.session_state.name = ""
    st.session_state.chat_history = []
    st.session_state.show_dropdown = False
    st.session_state.estimation_result = ""

if not st.session_state.name:
    st.subheader(get_ist_greeting() + "! 👋")
    st.session_state.name = st.text_input("Please Enter Your Name 🙇")
    if st.button("✅ Continue"):
        st.rerun()
    st.stop()

st.success(f"Welcome, {st.session_state.name}! 😊")

# ---------------------- UI: Topic & Sub-topic Selection ----------------------
topic = st.selectbox("Select Topic", ["Services", "Billing", "Booking", "General"])
sub_topic = st.selectbox("Select Sub-topic", ["Individual Product Shifting", "Complete House Shifting", "Estimation"])

if st.button("🎯 Submit Query"):
    st.session_state.chat_history.append(("bot", f"You selected Sub-Topic: **{sub_topic}** under Topic: **{topic}**."))
    log_to_mysql(st.session_state.name, f"Selected Topic: {topic} > {sub_topic}")
    if sub_topic.lower() == "estimation":
        st.info("📦 Scroll below for the estimation panel.")
        st.session_state.show_dropdown = True

# ---------------------- UI: Estimation Input & PDF ----------------------
if st.session_state.show_dropdown:
    st.markdown("## 🚚 Please Fill the Following Details for Estimation")
    house_size = st.selectbox("🏠 Select the house size:", ["1 BHK", "2 BHK", "3 BHK"])
    floor_from = st.selectbox("🧳 Select the loading floor:", ["Ground", "First", "Second", "Third"])
    floor_to = st.selectbox("🏡 Select the unloading floor:", ["Ground", "First", "Second", "Third"])
    vehicle = st.selectbox("🚛 Select your preferred vehicle:", ["Ape Tempo", "Tata Ace", "Eicher", "Lorry"])
    distance = st.number_input("📝 Enter the travel distance in kilometers (1–500):", min_value=1, max_value=500, value=10)

    # Store in session_state for PDF access
    st.session_state.house_size = house_size
    st.session_state.floor_from = floor_from
    st.session_state.floor_to = floor_to
    st.session_state.vehicle = vehicle
    st.session_state.distance = distance

    if st.button("📊 Get Estimation"):
        estimation = get_estimation_from_mysql(house_size, vehicle, floor_from, floor_to, distance)
        st.session_state.estimation_result = estimation
        st.markdown("## 📋 Estimation Result")
        st.code(estimation, language="markdown")
        log_to_mysql(st.session_state.name, estimation)

    if st.session_state.estimation_result:
        if st.button("📄 Generate PDF"):
            generate_pdf(
                st.session_state.name,
                st.session_state.estimation_result,
                st.session_state.house_size,
                st.session_state.vehicle
            )
            st.success("✅ PDF Generated Successfully!")

# ---------------------- Chat Input Processing ----------------------
query = st.chat_input("Type your message...")
if query:
    if not is_safe_input(query):
        st.warning("⚠️ Kindly rephrase your sentence properly to proceed further.")
    else:
        st.session_state.chat_history.append(("user", f"{st.session_state.name}: {query}"))
        answer = qa_chain.run(query)
        st.session_state.chat_history.append(("bot", f"i-Assist: {answer}"))
        log_to_mysql(st.session_state.name, query)
        log_to_mysql("bot", answer)

# ---------------------- Chat History Display ----------------------
for sender, msg in st.session_state.chat_history:
    with st.chat_message("🧑" if sender == "user" else "🤖"):
        st.markdown(msg)

# ---------------------- Exit Button ----------------------
if st.button("❌ See You Next Time"):
    st.session_state.clear()
    st.success("🙏 Thank you for interacting with i-Assist of Packers and Movers. Have a great day 😊 !!")
    st.stop()
