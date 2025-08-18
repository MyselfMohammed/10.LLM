# ---------------------- Form Input (Panel) ----------------------

import panel as pn         # Used for UI widgets and layouts in `collect_missing_inputs` (Panel-based UI)

def collect_missing_inputs(existing_values):
    house_sizes = ["1 BHK", "2 BHK", "3 BHK", "4 BHK", "Studio"]
    vehicles = ["Ape Tempo", "Tata Ace", "Eicher", "Lorry"]

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