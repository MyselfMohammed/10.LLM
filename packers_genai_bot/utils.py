# ---------------------- Standard Libraries ----------------------
import os                                           # For interacting with the operating system (e.g., folders, paths)
import re                                           # For regular expression operations like removing Unicode characters
from datetime import datetime, timedelta, timezone  # For managing date, time, timezone conversions (e.g., IST time)

# ---------------------- Third-Party Libraries ----------------------
import panel as pn         # Used for UI widgets and layouts in `collect_missing_inputs` (Panel-based UI)
import pandas as pd        # For data manipulation, reading Excel or CSV files, etc.
from fpdf import FPDF      # For generating PDF documents from text content
import mysql.connector     # To connect and interact with MySQL databases
import openai              # To use OpenAI APIs (e.g., ChatGPT, Moderation, Embeddings)
import streamlit as st     # For building interactive web apps (used in your main chatbot UI)

# ---------------------- Form Input (Panel) ----------------------
def collect_missing_inputs(existing_values):
    house_sizes = ["1 BHK", "2 BHK", "3 BHK", "4 BHK", "Studio"]
    vehicles = ["Small Truck", "Medium Truck", "Large Truck"]

    house_size = pn.widgets.Select(name="House Size", options=house_sizes, value=existing_values.get("house_size", house_sizes[0]))
    loading_floor = pn.widgets.IntInput(name="Loading Floor", value=existing_values.get("loading_floor", 0), start=0, end=20)
    unloading_floor = pn.widgets.IntInput(name="Unloading Floor", value=existing_values.get("unloading_floor", 0), start=0, end=20)
    vehicle = pn.widgets.Select(name="Vehicle Type", options=vehicles, value=existing_values.get("vehicle", vehicles[0]))
    distance_km = pn.widgets.IntInput(name="Distance (km)", value=existing_values.get("distance_km", 5), start=1, end=1000)

    widgets = {
        "house_size": house_size,
        "loading_floor": loading_floor,
        "unloading_floor": unloading_floor,
        "vehicle": vehicle,
        "distance_km": distance_km
    }

    layout = pn.Column(*widgets.values())
    return layout, widgets

# ---------------------- Normalization Utilities ----------------------
def normalize_house_size(size):
    mapping = {
        "1BHK": "1 BHK",
        "2BHK": "2 BHK",
        "3BHK": "3 BHK",
        "4BHK": "4 BHK",
        "Studio": "Studio"
    }
    return mapping.get(size.strip(), size)

def normalize_floor(floor):
    try:
        return int(floor)
    except:
        return 0

def normalize_vehicle(vehicle):
    mapping = {
        "Small Truck": "Small",
        "Medium Truck": "Medium",
        "Large Truck": "Large"
    }
    return mapping.get(vehicle.strip(), vehicle)

# ---------------------- Greeting Utility ----------------------
def get_ist_greeting():
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    hour = ist_now.hour
    if 0 <= hour < 12:
        return "Good Morning"
    elif 12 <= hour < 15:
        return "Good Afternoon"
    elif 15 <= hour < 20:
        return "Good Evening"
    else:
        return "Hello, a Wonderful Night"

# ---------------------- Input Safety Utility ----------------------
def is_safe_input(text):
    try:
        moderation = openai.Moderation.create(input=text)
        return not moderation['results'][0]['flagged']
    except Exception:
        return True

# ---------------------- Logger ----------------------
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

# ---------------------- Estimation Retrieval ----------------------
def get_estimation_from_mysql(house_size, vehicle, floor_from, floor_to, distance):
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT charges FROM packing_charges WHERE house_size = %s", (house_size,))
        packing = cursor.fetchone()
        packing_cost = packing['charges'] if packing else 0

        cursor.execute("SELECT loading FROM loading_unloading_charges WHERE house_size = %s AND floor = %s", (house_size, floor_from))
        load = cursor.fetchone()
        load_cost = load['loading'] if load else 0

        cursor.execute("SELECT unloading FROM loading_unloading_charges WHERE house_size = %s AND floor = %s", (house_size, floor_to))
        unload = cursor.fetchone()
        unload_cost = unload['unloading'] if unload else 0

        cursor.execute("SELECT standard_waiting_charges FROM waiting_charges WHERE house_size = %s", (house_size,))
        wait = cursor.fetchone()
        wait_cost = wait['standard_waiting_charges'] if wait else 0

        cursor.execute("""
            SELECT base_intra, per_km_intra, base_inter, per_km_inter
            FROM transportation_charges
            WHERE house_size = %s AND vehicle = %s
        """, (house_size, vehicle))
        t = cursor.fetchone()
        if t:
            intra = t['base_intra'] + t['per_km_intra'] * max(0, distance - 10)
            inter = t['base_inter'] + t['per_km_inter'] * max(0, distance - 10)
        else:
            intra = inter = 0

        cursor.close()
        conn.close()

        result = f"""
🧾 Estimated Cost Breakdown for {house_size} (Intra-City):
    Packing: {packing_cost}
    Loading (Floor {floor_from}): {load_cost}
    Unloading (Floor {floor_to}): {unload_cost}
    Waiting (6 hrs): {wait_cost}
    Transport (Intra): {intra}
    ==============================================================================
    Total (Intra): Rs.{packing_cost + load_cost + unload_cost + wait_cost + intra}
    ==============================================================================

🧾 Estimated Cost Breakdown for {house_size} (Inter-City):
    Packing: {packing_cost}
    Loading (Floor {floor_from}): {load_cost}
    Unloading (Floor {floor_to}): {unload_cost}
    Waiting (6 hrs): {wait_cost}
    Transport (Inter): {inter}
    ==============================================================================
    Total (Inter): Rs.{packing_cost + load_cost + unload_cost + wait_cost + inter}
    ==============================================================================
"""
        return result
    except Exception as e:
        return f"❌ Error fetching estimation: {e}"

# ---------------------- Misc Utilities ----------------------
def strip_unicode(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)

# ---------------------- PDF Generator ----------------------

def generate_pdf(customer_name, estimation_text, house_size, vehicle):
    from fpdf import FPDF
    from datetime import datetime, timedelta
    import os
    import re

    def sanitize_text(text):
        return text.encode('latin-1', 'replace').decode('latin-1')

    # Timestamp for filename
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    date_str = ist_now.strftime("%d_%m_%Y")
    time_str = ist_now.strftime("%I.%M_%p").upper()
    filename = f"Estimation_{date_str}_{time_str}_IST.pdf"

    # Save path
    output_dir = os.path.join(os.getcwd(), "Estimation")
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, sanitize_text(filename))

    # Company details
    company_info = {
        "name": "Packers and Movers",
        "address": "123, Mount Road\nChennai, Tamil Nadu - 600001",
        "gst": "GSTIN: ABCDEFGHIJLMNO123",
        "email": "e-Mail : p_and_m_support@email.com",
        "phone": "Phone : 1234567890"
    }

    # Start PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=10)

    # Red header
    pdf.set_fill_color(220, 50, 50)
    pdf.rect(10, 10, 190, 40, style='F')

    # Header - Left
    pdf.set_xy(10, 10)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(100, 10, sanitize_text(company_info["name"]), ln=0, align='L')
    
    # Header - Right
    pdf.set_font("Arial", 'B', 10)
    pdf.set_xy(110, 10)
    pdf.multi_cell(90, 5, sanitize_text(f"Customer Name : {customer_name}\nDate: {ist_now.strftime('%d %b %Y, %I:%M %p')}"), align='R')

    #Address block
    pdf.set_xy(10, 20)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 10)
    pdf.multi_cell(0, 5, sanitize_text(f"{company_info['address']}\n{company_info['gst']}\n{company_info['email']}\n{company_info['phone']}"), align='L')


    # Parse sections
    intra_lines, inter_lines = [], []
    section = None
    for line in estimation_text.splitlines():
        line = line.strip("` ").strip()
        if not line:
            continue
        if "Intra-City" in line:
            section = "intra"
        elif "Inter-City" in line:
            section = "inter"
        elif section == "intra":
            intra_lines.append(line)
        elif section == "inter":
            inter_lines.append(line)

    # Intra Section
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, sanitize_text("Estimated Cost Breakdown (For Intra-City):"), ln=1)
    pdf.set_font("Arial", '', 11)
    for line in intra_lines:
        if "Total" in line:
            amount = re.findall(r"\d[\d,]*\.?\d*", line)
            if amount:
                line = re.sub(r"₹\s*", "", line)
                line = re.sub(r"\d[\d,]*\.?\d*", f"{amount[0]}", line)
        else:
            line = line.replace("₹", "")
        pdf.cell(0, 6, sanitize_text(line), ln=1)

    # Inter Section
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, sanitize_text("Estimated Cost Breakdown (For Inter-City):"), ln=1)
    pdf.set_font("Arial", '', 11)
    for line in inter_lines:
        if "Total" in line:
            amount = re.findall(r"\d[\d,]*\.?\d*", line)
            if amount:
                line = re.sub(r"₹\s*", "", line)
                line = re.sub(r"\d[\d,]*\.?\d*", f"{amount[0]}", line)
        else:
            line = line.replace("₹", "")
        pdf.cell(0, 6, sanitize_text(line), ln=1)

    # Footer
    pdf.ln(10)
    pdf.set_fill_color(220, 50, 50)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, sanitize_text("********** Thank You !! Looking Forward To Serve You **********"), ln=1, align='C', fill=True)

    # Save PDF
    pdf.output(file_path)
