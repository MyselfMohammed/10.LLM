# ---------------------- Input Safety Utility ----------------------

import openai              # To use OpenAI APIs (e.g., ChatGPT, Moderation, Embeddings)

def is_safe_input(text):
    try:
        moderation = openai.Moderation.create(input=text)
        return not moderation['results'][0]['flagged']
    except Exception:
        return True

