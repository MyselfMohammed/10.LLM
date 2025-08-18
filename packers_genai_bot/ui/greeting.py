# ---------------------- Greeting Utility ----------------------

from datetime import datetime, timedelta, timezone  # For managing date, time, timezone conversions (e.g., IST time)

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
