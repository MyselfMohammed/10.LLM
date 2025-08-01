from fpdf import FPDF
from datetime import datetime
import pytz
import os

class EstimationPDF(FPDF):
    def __init__(self, customer_name):
        super().__init__()
        self.customer_name = customer_name
        self.ist = pytz.timezone("Asia/Kolkata")
        self.timestamp = datetime.now(self.ist)
        self.set_auto_page_break(auto=True, margin=20)
        self.red = (220, 20, 60)
        self.black = (0, 0, 0)

    def header(self):
        if self.page_no() == 1:
            # 🔴 Header Background
            self.set_fill_color(*self.red)
            self.rect(10, 10, 190, 40, style='F')

            # ✅ Add logo (top-right)
            try:
                self.image("logo_hope_ai.png", x=165, y=12, w=30)
            except Exception as e:
                print(f"⚠️ Couldn't add logo: {e}")

            # ✅ Left: Company Info
            self.set_text_color(255, 255, 255)
            self.set_font("Arial", 'B', 13)
            self.set_xy(12, 13)
            self.multi_cell(100, 6,
                "Packers and Movers (Powered By Hope-AI)\n"
                "123, Mount Road\n"
                "Chennai, Tamil Nadu - 600001\n"
                "GSTIN: ABCDEFGHIJLMNO123\n"
                "e-Mail : p_and_m_support@email.com\n"
                "Phone : 1234567890",
                border=0
            )

            # ✅ Right: Customer Info (below logo)
            self.set_font("Arial", '', 10)
            self.set_xy(135, 32)
            self.multi_cell(65, 6,
                f"Customer Name : {self.customer_name}\n"
                f"Date: {self.timestamp.strftime('%d %b %Y, %I:%M %p')}",
                align='R')

            self.ln(35)
        else:
            self.ln(10)

    def footer(self):
        # ✅ Page Border
        self.set_draw_color(*self.black)
        self.set_line_width(0.5)
        self.rect(10, 10, 190, 277)

        # ✅ Page Number
        self.set_y(-7)
        self.set_font("Arial", 'I', 8)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, 'C')

#---------------------------------------------------------------------------------------------------------------------------------------------------------------

def clean_text(text):
    return text.encode("latin-1", "ignore").decode("latin-1")

#---------------------------------------------------------------------------------------------------------------------------------------------------------------

def generate_estimation_pdf(text_output, customer_name="Customer"):
    # ✅ Prepare filename
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)
    timestamp = now.strftime("%d_%m_%Y_%I.%M_%p")
    filename = f"Packers_and_Movers_Estimation_{timestamp}.pdf"

    # ✅ Create PDF and add page (header auto-renders)
    pdf = EstimationPDF(customer_name)
    pdf.add_page()

    # ✅ Start content below header area
    pdf.set_xy(14, 55)

    for line in text_output.split('\n'):
        stripped = line.strip()

        if stripped.startswith("Estimated Cost Breakdown") or \
           stripped.startswith("For Your Kind Attention") or \
           stripped == "Transportation Charges:":
            pdf.ln(5)
            pdf.set_font("Arial", 'B', 11)
            pdf.multi_cell(182, 7, clean_text(stripped))
            pdf.set_font("Arial", size=10)
            continue

        pdf.multi_cell(182, 7, clean_text(stripped))

    # ✅ Thank You Note
    pdf.ln(10)
    pdf.set_fill_color(220, 20, 60)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, "********** Thank You !! Looking Forward To Serve You **********", ln=True, align='C', fill=True)

    # ✅ Save to Estimation folder
    os.makedirs("Estimation", exist_ok=True)
    pdf.output(f"Estimation/{filename}")
    print(f"✅ PDF generated: Estimation/{filename}")