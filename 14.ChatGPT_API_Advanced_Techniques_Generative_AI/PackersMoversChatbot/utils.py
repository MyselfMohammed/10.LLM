import os
import panel as pn  # GUI
pn.extension()
import sys
sys.path.append('../..') # Adds the project root to sys.path
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
# Load your optimized estimation data
import json

# Load the optimized JSON
with open("charges_categories.json", "r", encoding="utf-8") as f:
    estimation_data = json.load(f)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------

# --- 1. Normalization helpers ---
def normalize_house_size(house_size):
    """Convert variations like '1 BHK', '1BHK', 'One BHK' to a standard form (e.g. '1bhk')."""
    if not house_size:
        return ""
    hs = house_size.lower().replace(" ", "").replace(" ", "")
    # map spelled-out numbers to digits
    replacements = {"one": "1", "two": "2", "three": "3"}
    for word, digit in replacements.items():
        if hs.startswith(word):
            hs = hs.replace(word, digit, 1)
            break
    # ensure it ends with 'bhk'
    if not hs.endswith("bhk"):
        hs += "bhk"
    return hs

def normalize_floor(floor):
    """Map floor descriptions to standard keys."""
    if not floor:
        return ""
    floor_lc = floor.lower()
    if "ground" in floor_lc or "0" in floor_lc:
        return "Ground"
    if "first" in floor_lc or "1" in floor_lc:
        return "First"
    if "second" in floor_lc or "2" in floor_lc:
        return "Second"
    if "third" in floor_lc or "3" in floor_lc:
        return "Third"
    if "fourth" in floor_lc or "4" in floor_lc:
        return "Fourth"
    return floor.title()

def normalize_vehicle(vehicle):
    """Match vehicle names irrespective of case/spacing."""
    if not vehicle:
        return ""
    v_norm = vehicle.lower().replace(" ", "")
    for veh in estimation_data["charges"][0]["Transportation"].keys():
        if veh.lower().replace(" ", "") == v_norm:
            return veh
    # If no match found, return original
    return vehicle
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
# --- 2. Updated estimation function with PDF-friendly formatting ---
def calculate_estimation(house_size, loading_floor, unloading_floor, vehicle,
                         distance_km, waiting_hours=6):
    try:
        # Normalize inputs
        house_norm = normalize_house_size(house_size)
        load_floor_norm = normalize_floor(loading_floor)
        unload_floor_norm = normalize_floor(unloading_floor)
        vehicle_norm = normalize_vehicle(vehicle)

        # Find the matching house-size entry in the JSON
        charge_data = next(
            item for item in estimation_data["charges"]
            if normalize_house_size(item["House Size"]) == house_norm
        )

        packing_cost = charge_data["Packing"]
        loading_cost = charge_data["Loading & Unloading"][load_floor_norm]["Loading"]
        unloading_cost = charge_data["Loading & Unloading"][unload_floor_norm]["Unloading"]

        std_waiting_hrs = 6
        base_waiting_cost = charge_data["Waiting Charges"]["Standard (6 Hrs)"]
        addon_waiting_cost_per_hr = charge_data["Waiting Charges"]["Add-on per Hr"]
        addon_waiting_hours = max(0, waiting_hours - std_waiting_hrs)
        addon_waiting_charge = addon_waiting_hours * addon_waiting_cost_per_hr

        def calculate_transport(city_type):
            base_key = f"10 Kms - {city_type}"
            addon_key = f"Add-on/Km - {city_type}"
            base = charge_data["Transportation"][vehicle_norm][base_key]
            addon_rate = charge_data["Transportation"][vehicle_norm][addon_key]
            extra_km = max(0, distance_km - 10)
            addon_charge = extra_km * addon_rate
            total = base + addon_charge
            return base, addon_rate, extra_km, addon_charge, total

        # Calculate for intra- and inter-city
        base_t_intra, rate_intra, extra_km_intra, addon_t_intra, total_t_intra = calculate_transport("Intra-city")
        total_intra = packing_cost + loading_cost + unloading_cost + (base_waiting_cost + addon_waiting_charge) + total_t_intra

        base_t_inter, rate_inter, extra_km_inter, addon_t_inter, total_t_inter = calculate_transport("Inter-city")
        total_inter = packing_cost + loading_cost + unloading_cost + (base_waiting_cost + addon_waiting_charge) + total_t_inter

        # Compose output
        output = ""  # Reset output

        output += f"Estimated Cost Breakdown (For Intra-City):\n"
        output += f"Packing Cost: ₹{packing_cost}\n"
        output += f"Loading Cost from {load_floor_norm} Floor: ₹{loading_cost}\n"
        output += f"Unloading Cost to {unload_floor_norm} Floor: ₹{unloading_cost}\n"
        output += f"Base Waiting Charges (6 hrs): ₹{base_waiting_cost}\n"
        output += f"Add-on Waiting Hours ({addon_waiting_hours} - Hour(s)) and its Charges: ₹{addon_waiting_charge}\n"
        output += f"Base Transport Charges (10 km) - {vehicle_norm} (Intra-city): ₹{base_t_intra}\n"
        output += f"Add-on Transport ({extra_km_intra:02} - Km(s)) and Its Charges: ₹{addon_t_intra}\n"
        output += f"Total Transport Cost: ₹{total_t_intra}\n"
        output += f"{'='*66}\n"
        output += f"Total Estimated Cost for Intra-City Transition : ₹{total_intra}\n"
        output += f"{'='*66}\n\n"

        output += f"Estimated Cost Breakdown (For Inter-City):\n"
        output += f"Packing Cost: ₹{packing_cost}\n"
        output += f"Loading Cost from {load_floor_norm} Floor: ₹{loading_cost}\n"
        output += f"Unloading Cost to {unload_floor_norm} Floor: ₹{unloading_cost}\n"
        output += f"Base Waiting Charges (6 hrs): ₹{base_waiting_cost}\n"
        output += f"Add-on Waiting Hours ({addon_waiting_hours} - Hour(s)) and its Charges: ₹{addon_waiting_charge}\n"
        output += f"Base Transport Charges (10 km) - {vehicle_norm} (Inter-city): ₹{base_t_inter}\n"
        output += f"Add-on Transport ({extra_km_inter:02} - Km(s)) and Its Charges: ₹{addon_t_inter}\n"
        output += f"Total Transport Cost: ₹{total_t_inter}\n"
        output += f"{'='*66}\n"
        output += f"Total Estimated Cost for Inter-City Transition : ₹{total_inter}\n"
        output += f"{'='*66}\n\n"

        output += f"For Your Kind Attention on Add-on Breakdown:\n"
        output += f"Waiting Charges:\n"
        output += f"  Add-on Waiting Charges Per Hour (Intra-City): ₹{addon_waiting_cost_per_hr}\n"
        output += f"  Add-on Waiting Charges Per Hour (Inter-City): ₹{addon_waiting_cost_per_hr}\n\n"
        output += f"Transportation Charges:\n"
        output += f"  Add-on Transport Charges Per Km (Intra-City): ₹{rate_intra}\n"
        output += f"  Add-on Transport Charges Per Km (Inter-City): ₹{rate_inter}"

        return output.strip()

    except Exception as e:
        return f"❌ Error occurred: {str(e)}"
#---------------------------------------------------------------------------------------------------------------------------------------------------------------

required_keys = ["house_size", "loading_floor", "unloading_floor", "vehicle", "distance_km"]

# Jupyter-friendly version using Panel's reactive model
def ask_missing_value(key):
    dropdown_options = {
        "house_size": ["1BHK", "2BHK", "3BHK"],
        "loading_floor": ["Ground", "First", "Second", "Third"],
        "unloading_floor": ["Ground", "First", "Second", "Third"],
        "vehicle": ["Ape Tempo", "Tata Ace", "Eicher", "Lorry"],
    }

    prompts = {
        "house_size": "🏠 Select the house size:",
        "loading_floor": "📦 Select the loading floor:",
        "unloading_floor": "🏠 Select the unloading floor:",
        "vehicle": "🚚 Select your preferred vehicle:",
        "distance_km": "📏 Enter the travel distance in kilometers (1–500):"
    }

    value_holder = pn.pane.Markdown()

    def create_submit_block(widget):
        submit = pn.widgets.Button(name="Submit", button_type="primary")
        result_pane = pn.pane.Markdown()

        def on_submit(event):
            result_pane.object = f"✅ Selected: **{widget.value}**"
            pn.state.param_value = widget.value

        pn.state.param_value = None
        submit.on_click(on_submit)

        return pn.Column(widget, submit, result_pane)

    if key == "distance_km":
        km_input = pn.widgets.IntSlider(
            name=prompts[key], start=1, end=500, step=1, value=10
        )
        return create_submit_block(km_input)

    elif key in dropdown_options:
        dropdown = pn.widgets.Select(name=prompts[key], options=dropdown_options[key])
        return create_submit_block(dropdown)

    else:
        text_input = pn.widgets.TextInput(name=prompts.get(key, f"Please enter value for {key}: "))
        return create_submit_block(text_input)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------

def collect_missing_inputs(params):
    dropdown_options = {
        "house_size": ["1BHK", "2BHK", "3BHK"],
        "loading_floor": ["Ground", "First", "Second", "Third"],
        "unloading_floor": ["Ground", "First", "Second", "Third"],
        "vehicle": ["Ape Tempo", "Tata Ace", "Eicher", "Lorry"],
    }

    prompts = {
        "house_size": "🏠 Select the house size:",
        "loading_floor": "📦 Select the loading floor:",
        "unloading_floor": "🏠 Select the unloading floor:",
        "vehicle": "🚚 Select your preferred vehicle:",
        "distance_km": "📏 Enter the travel distance in kilometers (1–500):"
    }

    widget_refs = {}
    form_items = []

    for key in required_keys:
        if key == "distance_km":
            widget = pn.widgets.IntInput(name=prompts[key], start=1, end=500, value=10)
        elif key in dropdown_options:
            widget = pn.widgets.Select(name=prompts[key], options=dropdown_options[key])
        else:
            widget = pn.widgets.TextInput(name=prompts[key])
        widget_refs[key] = widget
        form_items.append(widget)

    return pn.Column("## 🚛 Please fill the following details for estimation", *form_items), widget_refs



#---------------------------------------------------------------------------------------------------------------------------------------------------------------