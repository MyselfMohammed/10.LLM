
# Packers and Movers GenAI Chatbot – End-to-End Documentation

---

## Introduction

This project is a **Packers and Movers Domain GenAI Chatbot** using Retrieval-Augmented Generation (RAG) with OpenAI LLM, FAISS for semantic retrieval, structured/interactive forms, estimation PDF generation, and more.  
It demonstrates production-ready GenAI skills and covers a real-life scenario with intelligent estimation, dynamic knowledge, and user-centric UI.

---

## System Architecture & Flow Diagram

### **System Flow (Mermaid Syntax):**

```mermaid
flowchart TD
    A --> [User Input (Chat/UI Forms)] --> B[Input Validation]
    B --> C{Request Type?}
    C -- "Info/FAQ" --> D[Retriever: FAISS Semantic Search (vectordb/)]
    C -- "Estimation" --> E[Estimation Module (core/estimation.py)]
    D --> F[Context Passed to LLM (OpenAI API)]
    F --> G[Response Rendered in UI]
    E --> H[PDF Estimation Generated (core/pdf_generator.py)]
    H --> I[PDF Download Link in UI]
    G --> J[MySQL/Logs (core/mysql_logger.py)]
    H --> J
    C -- "Form Submission" --> K[Input Normalization (core/normalizer.py)]
    K --> E
```

---

## Project Structure

```
packers_genai_bot/
    .env, requirements.txt, app.py
    config/         # env/config management
    core/           # Main business logic, estimation, logging, safety checks
    data/           # XLSX and PDF knowledge base
    Estimation/     # Output PDF estimates
    rag/            # RAG chain, vector ingest
    ui/             # UI modules (chat, forms, theme)
    utils/          # Helpers, session state
    vectordb/       # FAISS index files
```

---

## Installation & Environment Setup

### Requirements

- Python 3.10+ (Recommended)
- pip, virtualenv
- OpenAI API key (and possibly MySQL DB access)

### Steps

```bash
# 1. Navigate to the project folder
cd packers_genai_bot

# 2. Set up virtual environment
python -m venv .venv
source .venv/bin/activate      # or .venv\Scripts\activate on Windows

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Set up your API keys and secrets in .env and config/env.py

# 5. (Optional) Install system dependencies for FAISS if needed

# 6. Ingest data and build vector index
python rag/ingest.py

# 7. (Optional) Set up and test database for logging, if used

# 8. Start the chatbot
streamlit run app.py
```

---

## Data Sources & Indexing

- **data/golder_faqs_by_categories.xlsx**  
  Structured packers/movers FAQs and policies.

- **data/non-admissible-expenses.pdf**  
  Unstructured knowledge base (PDFs).

- **assistant_instructions.xlsx**  
  Instructions for agent/assistant (possibly prompt-engineering data).

- **vectordb/packers_faiss/index.faiss + index.pkl**  
  FAISS vector store for semantic retrieval.

- **Estimation/**  
  Stores generated PDF cost estimates for users.

---

## How the Chatbot Works

1. **User enters a query** (text chat or form input).

2. **Input is validated** and categorized as either:
    - FAQ/information request (handled via RAG)
    - Estimation request (triggers estimation pipeline)
    - Structured form (form → normalization → estimation)

3. **For information requests:**  
    - The query is semantically searched against the vector database.
    - Retrieved context is sent to OpenAI LLM for a relevant answer.

4. **For estimation:**  
    - Details are normalized.
    - Business logic in `core/estimation.py` generates an estimate.
    - `core/pdf_generator.py` creates a custom PDF with estimate and details.
    - PDF download link is presented in the chat UI.

5. **All actions and chats can be logged** (MySQL or local logs).

6. **Session state and forms** handled for smooth multi-step UX.

---

## Code Modules Breakdown

### **Core Logic (`core/`)**
- `estimation.py`: Core logic for estimation, cost calculation, and orchestrating user estimation workflow.
- `pdf_generator.py`: Generates PDF cost estimate for user requests.
- `message_handler.py`: Handles chat messages, routes intent to correct submodule.
- `mysql_logger.py`: (Optional) Logs conversation, estimation, and actions to a MySQL DB.
- `normalizer.py`: Standardizes/validates user input (e.g., city names, item lists).
- `safety_check.py`: Ensures safety and moderation of input (basic prompt/response filtering).

### **RAG Modules (`rag/`)**
- `ingest.py`: Processes XLSX/PDF, chunks text, generates embeddings, builds FAISS index.
- `chain.py`: Implements retrieval-augmented generation flow for user queries.

### **UI (`ui/`)**
- `chat_display.py`: Shows conversation in chat format.
- `forms.py`, `form_inputs.py`: Interactive forms for estimation, user onboarding, etc.
- `greeting.py`, `onboarding.py`: Welcomes and guides users.
- `theme.py`: Customizes UI appearance.

### **Utils/Config**
- `utils/helpers.py`: Reusable utility functions.
- `utils/session_state.py`: Session state management.
- `config/env.py` + `.env`: API keys, environment variables.

### **Other**
- `Estimation/`: All generated PDF estimates.
- `.ipynb_checkpoints/`: (Ignore) Jupyter checkpoints from development.
- `requirements.txt`: Python dependencies.

---

## Running the Chatbot

### **To launch chat UI:**
```bash
streamlit run app.py
```
- Open the provided URL in your browser.
- Interact with the Packers & Movers chatbot for Q&A or estimation.

### **To build/rebuild the vector index:**
```bash
python rag/ingest.py
```
- Processes your XLSX/PDF knowledge base.

```

---

## Testing & QA Validation

- **Estimation:** Try form submission with different details; check generated PDFs in `Estimation/`.
- **FAQ/RAG:** Ask insurance/movers questions; verify accuracy and completeness.
- **Input edge cases:** Try typos, partial input, multi-step forms.
- **Logging:** Check MySQL logs or app logs if enabled.

---

## Logs & Debugging

- **MySQL logging:** If set up, all interactions are logged.

- **Estimation PDFs:** All output is in `Estimation/`.

- **Console logs:** Streamlit/app log shows real-time events.

- **Debugging Tips:**
    - Re-run `rag/ingest.py` after knowledge base update.
    - Inspect logs for errors or broken flows.
    - Test API/DB credentials in `.env` and `config/env.py`.

---

## Project Experience Insights

- **Real-world GenAI application:**  
  Handles both knowledge retrieval (RAG) and custom business workflow (estimation).

- **Hybrid knowledge:**  
  Supports both structured and unstructured sources.

- **Advanced features:**  
  PDF report generation, semantic search, input normalization, chat+forms, logging.

- **Production best practices:**  
  Config separation, logging, session state, modular code.

---

## Possible Extensions

- Add live pricing APIs for dynamic estimation.
- Multilingual support for broader reach.
- Enhanced UI/UX with more visualizations.
- User authentication and history tracking.
- Deploy as a cloud or mobile app.
- Integration with CRM or real user bookings.

---


