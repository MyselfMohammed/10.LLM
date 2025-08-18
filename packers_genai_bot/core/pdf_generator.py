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
