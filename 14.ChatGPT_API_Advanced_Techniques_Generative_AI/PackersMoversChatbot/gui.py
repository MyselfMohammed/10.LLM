
import gradio as gr
from utils import extract_cost_params, calculate_estimation
from moderation import moderate_input
from pdf_generator import generate_estimation_pdf

def process_query(user_input, customer_name):
    # Step 1: Moderation Check
    flagged, reasons = moderate_input(user_input)
    if flagged:
        return f"⚠️ Input flagged as unsafe.
Reasons: {reasons}", None

    # Step 2: Extract Parameters
    params = extract_cost_params(user_input)
    if not params:
        return "❌ Could not extract parameters from your input. Please rephrase.", None

    # Step 3: Remove city_type if present (not used)
    params.pop("city_type", None)

    # Step 4: Estimate Cost
    estimation_result = calculate_estimation(**params)

    return estimation_result, (params, estimation_result, customer_name)

def generate_pdf_trigger(data):
    if data is None:
        return "❌ Please first run an estimation."
    params, estimation_result, customer_name = data
    generate_estimation_pdf(estimation_result, customer_name=customer_name)
    return "✅ PDF generated successfully and saved in your working directory."

# Gradio Interface
with gr.Blocks(title="Packers & Movers Estimator") as demo:
    gr.Markdown("## 📦 Packers & Movers Estimation Assistant")
    gr.Markdown("Enter your shifting details below:")

    user_input = gr.Textbox(label="Your Query", placeholder="e.g. Shift 2BHK from ground to 2nd floor using Tata Ace, 15 km, 7 hours waiting")
    customer_name = gr.Textbox(label="Customer Name", placeholder="Enter your name", value="Customer")

    with gr.Row():
        submit_btn = gr.Button("Estimate Cost")
        pdf_btn = gr.Button("Generate PDF")

    output = gr.Textbox(label="Estimated Cost", lines=15)
    pdf_status = gr.Textbox(label="PDF Status")

    data_state = gr.State()

    submit_btn.click(fn=process_query, inputs=[user_input, customer_name], outputs=[output, data_state])
    pdf_btn.click(fn=generate_pdf_trigger, inputs=data_state, outputs=pdf_status)

demo.launch()
