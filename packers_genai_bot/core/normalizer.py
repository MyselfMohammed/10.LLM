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
