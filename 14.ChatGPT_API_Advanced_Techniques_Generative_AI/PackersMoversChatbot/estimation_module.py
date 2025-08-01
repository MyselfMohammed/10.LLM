from utils import calculate_estimation, normalize_house_size, normalize_floor, normalize_vehicle, collect_missing_inputs
from pdf_generator import generate_estimation_pdf
import panel as pn
pn.extension()

def run_estimation_flow(customer_name="Customer"):
    # Step 1: Build UI and capture widgets
    layout, widget_refs = collect_missing_inputs({})

    # Step 2: Output and banner
    output_panel = pn.pane.Markdown()
    pdf_status_panel = pn.pane.Markdown("", width=250)
    info_banner = pn.pane.Markdown("🚛 Please Fill the Following Details for Estimation")

    # Step 3: PDF components (created but only displayed on submit)
    pdf_btn = pn.widgets.Button(name="📄 Download PDF", button_type="success")
    pdf_row = pn.Row(pdf_btn, pdf_status_panel)
    
    # Step 4: Submit button and logic
    submit_btn = pn.widgets.Button(name="Get Estimation", button_type="primary")

    def on_submit(event):
        params = {k: w.value for k, w in widget_refs.items()}

        params["house_size"] = normalize_house_size(params.get("house_size"))
        params["loading_floor"] = normalize_floor(params.get("loading_floor"))
        params["unloading_floor"] = normalize_floor(params.get("unloading_floor"))
        params["vehicle"] = normalize_vehicle(params.get("vehicle"))
        params["distance_km"] = int(params.get("distance_km", 0))
        params["waiting_hours"] = 6

        accepted_keys = ["house_size", "loading_floor", "unloading_floor", "vehicle", "distance_km", "waiting_hours"]
        filtered_params = {k: v for k, v in params.items() if k in accepted_keys}

        result = calculate_estimation(**filtered_params)
        output_panel.object = f"### 📦 Estimation Result\n```\n{result}\n```"

        # Show PDF button once estimation is done
        if pdf_row not in layout.objects:
            layout.append(pdf_row)

        def generate_pdf_click(event):
            generate_estimation_pdf(result, customer_name=customer_name)
            pdf_status_panel.object = "✅ PDF Generated Successfully!"

        pdf_btn.on_click(generate_pdf_click)

    submit_btn.on_click(on_submit)

    # ✅ Final layout (outside callback)
    full_ui = pn.Column(
        info_banner,
        layout,
        submit_btn,
        output_panel
    )

    return full_ui
