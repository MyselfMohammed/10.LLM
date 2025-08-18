import os
import sys
from dotenv import load_dotenv
import importlib.util


def green(msg):
    print(f"\033[92m{msg}\033[0m")


def red(msg):
    print(f"\033[91m{msg}\033[0m")


def check_env():
    print("🔎 Checking .env and secrets...")
    load_dotenv()
    required_keys = ["OPENAI_API_KEY", "FAISS_DB_PATH"]
    missing = [k for k in required_keys if not os.getenv(k)]
    if missing:
        red(f"❌ Missing required .env keys: {', '.join(missing)}")
        return False
    green("✅ .env secrets loaded.")
    return True


def check_api_key():
    print("🔎 Checking OpenAI API key...")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or not api_key.startswith("sk-"):
        red("❌ OPENAI_API_KEY looks invalid!")
        return False
    green("✅ API key format looks OK.")
    return True


def check_files():
    print("🔎 Checking data/index files...")
    data_folder = os.path.join(os.path.dirname(__file__), "data")
    faiss_path = os.getenv("FAISS_DB_PATH", "faiss_medrisk_index")
    ok = True
    if not os.path.exists(data_folder) or not os.listdir(data_folder):
        red("❌ No files in data/ folder!")
        ok = False
    else:
        green("✅ Data files present.")
    if not os.path.exists(faiss_path):
        red(f"❌ FAISS index file '{faiss_path}' not found.")
        ok = False
    else:
        green("✅ FAISS index found.")
    return ok


import importlib.util

def red(msg): print(f"\033[91m{msg}\033[0m")
def green(msg): print(f"\033[92m{msg}\033[0m")

def check_imports():
    print("🔎 Checking Python dependencies...")
    # Map of PyPI names to their Python import names
    required = {
        "python-dotenv": "dotenv",
        "scikit-learn": "sklearn",
        "streamlit": "streamlit",
        "openai": "openai",
        "langchain": "langchain",
        "langchain-community": "langchain_community",
        "langchain-openai": "langchain_openai",
        "unstructured": "unstructured",
        "networkx": "networkx",
        "openpyxl": "openpyxl",
        "python-docx": "docx",
        "msoffcrypto-tool": "msoffcrypto"
    }
    ok = True
    for pip_name, import_name in required.items():
        if importlib.util.find_spec(import_name) is None:
            red(f"❌ Missing Python package: {pip_name} (import as '{import_name}')")
            ok = False
    if ok:
        green("✅ All dependencies installed.")
    return ok


def check_model_response():
    print("🔎 Testing LLM/RAG pipeline (mock check)...")
    try:
        # Import your core RAG handler (update path if needed)
        from core.rag_engine import get_rag_chain

        chain = get_rag_chain()
        resp = chain("What is covered by Medrisk insurance?")
        if isinstance(resp, dict) and ("result" in resp or "answer" in resp):
            green("✅ Model responds to queries.")
            return True
        else:
            red("❌ Model did not return an expected response.")
            return False
    except Exception as e:
        red(f"❌ Model pipeline test failed: {e}")
        return False


def main():
    all_ok = True
    print("==== Medrisk GenAI CLI QA Checks ====")
    all_ok &= check_env()
    all_ok &= check_api_key()
    all_ok &= check_files()
    all_ok &= check_imports()
    # Optional: Run the model only if above checks pass
    if all_ok:
        all_ok &= check_model_response()
    print("\n==== RESULT ====")
    if all_ok:
        green("🎉 All QA checks PASSED!")
        sys.exit(0)
    else:
        red("Some checks FAILED. See above for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()
