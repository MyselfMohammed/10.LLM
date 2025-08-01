# moderation.py

# 📦 Import the OpenAI package
from openai import OpenAI

# 🔐 Set up the OpenAI client using your API key
# (Replace "your-api-key" with your actual OpenAI key)

# ✅ Set your OpenAI API key
Gen_Learn = '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'

# ✅ Initialize OpenAI client
client = OpenAI(api_key=Gen_Learn)

def moderate_input(text):
    try:
        response = client.moderations.create(input=text)
        result = response.results[0]
        return result.flagged, result.categories
    except Exception as e:
        return False, {"error": str(e)}
