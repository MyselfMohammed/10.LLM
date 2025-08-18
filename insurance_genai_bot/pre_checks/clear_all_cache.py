import os
import shutil

# 1. Clear Streamlit cache (works for Streamlit v1.22+)
try:
    import streamlit as st

    st.cache_data.clear()
    st.cache_resource.clear()
    print("[OK] Streamlit cache cleared.")
except Exception:
    print("[Info] Streamlit cache may already be clear, or Streamlit not installed.")

# 2. Remove FAISS index file
# Update this path if your index file has a different name
FAISS_DB_PATH = "faiss_medrisk_index"
if os.path.exists(FAISS_DB_PATH):
    try:
        os.remove(FAISS_DB_PATH)
        print(f"[OK] FAISS vector index '{FAISS_DB_PATH}' deleted.")
    except Exception as e:
        print(f"[WARN] Couldn't delete FAISS index: {e}")
else:
    print(f"[Info] FAISS index '{FAISS_DB_PATH}' not found, nothing to clear.")

# 3. Delete all __pycache__ folders recursively


def remove_pycache_dirs(root_dir="."):
    removed = 0
    for root, dirs, files in os.walk(root_dir):
        if "__pycache__" in dirs:
            pycache_path = os.path.join(root, "__pycache__")
            shutil.rmtree(pycache_path)
            removed += 1
            print(f"[OK] Removed: {pycache_path}")
    if removed == 0:
        print("[Info] No __pycache__ folders found.")


remove_pycache_dirs()

print("\nAll caches cleared. You can now safely run your app.")
