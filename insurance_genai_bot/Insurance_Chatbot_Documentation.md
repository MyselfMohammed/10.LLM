
# Insurance Domain Chatbot – End-to-End Documentation

## 1. Project Overview & Architecture

**Goal:**  
This project implements a GenAI-powered insurance domain chatbot using Retrieval-Augmented Generation (RAG), combining LLM (OpenAI API), FAISS for vector search, and support for both PDF and Excel knowledge bases.

**Architecture Highlights:**
- **Retrieval-Augmented Generation (RAG):**

    - Uses FAISS vector store for fast, semantic search over insurance PDFs & FAQs.
    - Supports dynamic context retrieval from both structured (Excel) and unstructured (PDF) sources.
- **LLM-based Chatbot:**
    - Integrates with OpenAI API for response generation.
- **Streamlit-based UI:**
    - User-friendly frontend with chat bubbles, history, input bar, and onboarding.
- **Modular QA Validation:**
    - Automated test batch runner, pipeline health checks, and result logging.
- **Extensible:**
    - Easily plug in more data or swap LLMs.

---

## 2. Installation & Environment Setup

**Requirements:**
- Python 3.10+ (Recommended)
- pip, virtualenv (recommended)
- Access to OpenAI API

**Steps:**
```bash
# 1. Clone or unzip the project
cd insurance_genai_bot

# 2. Set up virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -r config/requirements.txt

# 4. Set environment variables
# Edit config/env.py with your OpenAI API key and any other secrets

# 5. [Optional] Install additional system dependencies for FAISS if needed
# On Ubuntu: sudo apt-get install libopenblas-dev

# 6. (First time only) Build/rebuild FAISS index from PDF/Excel
python core/rag_engine.py  # or via Streamlit UI

# 7. Run pre-checks to clear cache & ensure health
python pre_checks/pre_checks.py

# 8. Start the chatbot
streamlit run app.py

# 9. Run QA
python qa/qa_batch_runner.py
```

---

## 3. Data Sources & Indexing

- **data/golder_faqs_by_categories.xlsx**  
  Insurance FAQs, policies, and structured knowledge.
- **data/non-admissible-expenses.pdf**  
  Example of unstructured insurance guidelines.

**Indexing:**
- **core/rag_engine.py** loads and processes PDFs/Excels, chunks text, and builds FAISS index (`faiss_medrisk_index/`).
- **index.faiss** and **index.pkl** are used for semantic retrieval during chat.

---

## 4. Code Modules Breakdown

### 4.1 Core Logic (`core/`)
- **chat_handler.py:**  
  Main orchestrator for user queries, calls retrieval, and LLM response.
- **chat_logic.py:**  
  Business rules, dialogue flow, and response enrichment.
- **rag_engine.py:**  
  All logic for PDF/Excel loading, text chunking, embeddings, and FAISS management.
- **session_manager.py:**  
  User session tracking for context continuity.
- **user_input_validation.py:**  
  Pre-LLM checks on input quality, filtering, etc.

### 4.2 UI (`ui/`)
- **chat_bubbles.py, chat_history.py, input_bar.py, greeting.py, onboarding.py, theme.py**
  Each handles a specific UI component in Streamlit: chat formatting, input capture, onboarding screens, theming.

### 4.3 QA & Validation (`qa/`)
- **response_quality.py, dataset_coverage.py, pipeline_health.py, observability.py, qa_batch_runner.py**  
  Automated test framework for running batch QA, tracking response metrics, pipeline health, and generating coverage reports.
- **qa_input/qa_test_questions.xlsx:**  
  List of test questions.
- **qa_output/QA_Results_*.xlsx:**  
  Results log, suitable for audit or continuous improvement.

### 4.4 Utils & Config
- **utils/**  
  Helpers for Excel, file ops, session state.
- **config/env.py:**  
  Set your API keys and environment configs.
- **config/requirements.txt:**  
  All Python dependencies listed here.

---

## 5. How to Run the Bot

**Start the Chatbot (Streamlit UI):**
```bash
streamlit run app.py
```
- Open browser to the provided URL.
- Interact with the insurance chatbot.
- UI will show chat bubbles, allow file uploads, and maintain chat history.

**Command-Line QA Batch:**
```bash
python qa/qa_batch_runner.py
```
- Runs through all questions in `qa_input/qa_test_questions.xlsx` and logs results to `qa_output/`.

---

## 6. Testing & QA Validation

- **Automated QA**:  
  - Validate completeness, correctness, and min length for answers.
  - Logs detailed output for review.
- **Pipeline Health Checks:**  
  - Check data coverage, embedding status, and retrieval accuracy.
- **Manual Test:**  
  - Use UI and interact with various insurance scenarios to check real responses.

---

## 7. Logs & Debugging

- **logs/qa.log**
  - Runtime logs, errors, and QA test outputs.
- **logs/__init__.py**
  - Ensures logging module is importable.
- **Debugging Tips:**
  - Clear all caches: `python pre_checks/clear_all_cache.py`
  - Inspect logs for any error tracebacks or missing data.

---

## 8. Project Experience Insights

- **Real-world Project Environment:**  
  - Mimics a full-stack, production-grade RAG chatbot.
  - Modular, clean code and QA-ready for audit.
  - Covers both structured (Excel) and unstructured (PDF) sources—a key RAG challenge.
- **Demonstrates:**
  - LLM integration (OpenAI API)
  - Custom retriever (FAISS)
  - Batch QA for output validation
  - Streamlit UI for demo

---

## 9. Possible Extensions

- Add more domain knowledge sources.
- Connect with real-time policy APIs.
- Support multi-lingual retrieval.
- Swap LLM backend (Azure, local LLM).
- Enhance UI with authentication, chatbot avatars, advanced analytics.
- Deploy as web app with Docker/GCP/AWS.

---


