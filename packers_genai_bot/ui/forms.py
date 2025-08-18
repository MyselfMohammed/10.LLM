# Estimation UI Input form

import streamlit as st
from core.estimation import get_estimation_from_mysql
from core.pdf_generator import generate_pdf

def render_estimation_form():
    """Render the estimation form and handle input + button interaction."""
    st.markdown("## 🚚 Please Fill the Following Details for Estimation")

    house_size = st.selectbox("🏠 Select the house size:", ["1 BHK", "2 BHK", "3 BHK"], key="est_house_size")
    floor_from = st.selectbox("🧳 Select the loading floor:", ["Ground", "First", "Second", "Third"], key="est_floor_from")
    floor_to = st.selectbox("🏡 Select the unloading floor:", ["Ground", "First", "Second", "Third"], key="est_floor_to")
    vehicle = st.selectbox("🚛 Select your preferred vehicle:", ["Ape Tempo", "Tata Ace", "Eicher", "Lorry"], key="est_vehicle")
    distance = st.number_input("📝 Enter the travel distance in kilometers (1–500):", min_value=1, max_value=500, value=10, key="est_distance")

    st.session_state.house_size = house_size
    st.session_state.floor_from = floor_from
    st.session_state.floor_to = floor_to
    st.session_state.vehicle = vehicle
    st.session_state.distance = distance

    if st.button("📊 Get Estimation", key="btn_get_estimation"):
        estimation = get_estimation_from_mysql(house_size, vehicle, floor_from, floor_to, distance)
        st.session_state.estimation_result = estimation
        st.session_state.estimation_done = True
        st.rerun()

def render_estimation_result():
    """Render the estimation result and PDF download option."""
    st.markdown("## 📋 Estimation Result")
    st.code(st.session_state.estimation_result, language="markdown")

    if st.button("📄 Generate PDF", key="btn_generate_pdf"):
        generate_pdf(
            st.session_state.name,
            st.session_state.estimation_result,
            st.session_state.house_size,
            st.session_state.vehicle
        )
        st.success("✅ PDF Generated Successfully!")
