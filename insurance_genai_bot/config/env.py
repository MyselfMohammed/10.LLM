import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FAISS_DB_PATH = os.getenv("FAISS_DB_PATH", "faiss_medrisk_index")
DATA_FOLDER = os.path.join(os.path.dirname(__file__), "..", "data")
