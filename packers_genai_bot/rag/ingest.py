# Import standard libraries
import os  # For interacting with the file system
import pandas as pd  # For reading Excel files
from dotenv import load_dotenv  # For loading environment variables from a .env file

# Import LangChain modules
from langchain.text_splitter import RecursiveCharacterTextSplitter  # For breaking documents into chunks
from langchain_openai import OpenAIEmbeddings  # ✅ Modern import for OpenAI embeddings
from langchain_community.vectorstores import FAISS  # FAISS is used to store and search vector embeddings
from langchain.docstore.document import Document  # LangChain document wrapper with content and metadata

# ✅ Load environment variables (like OPENAI_API_KEY) from a `.env` file into environment
load_dotenv()

# ✅ Path to the Excel knowledge base file
excel_path = "data/assistant_instructions.xlsx"

# ✅ Output path where the FAISS vector store will be saved
faiss_path = "vectordb/packers_faiss"

# ✅ Read all sheets from the Excel file into a dictionary of DataFrames
xls = pd.read_excel(excel_path, sheet_name=None)

# ✅ Initialize an empty list to store LangChain Document objects
documents = []

# ✅ Loop through each sheet in the Excel file
for sheet, df in xls.items():
    content = df.to_string(index=False)  # Convert the DataFrame to plain text
    metadata = {"source": sheet}  # Optional metadata to track which sheet it came from
    documents.append(Document(page_content=content, metadata=metadata))  # Create a LangChain Document

# ✅ Initialize the text splitter to break large documents into chunks of 500 characters with 50-character overlap
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

# ✅ Apply the splitter to all documents
split_docs = splitter.split_documents(documents)

# ✅ Initialize OpenAI Embeddings using your API key from .env or environment variable
embeddings = OpenAIEmbeddings()

# ✅ Create a FAISS vector index from the embedded split documents
faiss_index = FAISS.from_documents(split_docs, embeddings)

# ✅ Ensure the output folder exists
os.makedirs(os.path.dirname(faiss_path), exist_ok=True)

# ✅ Save the FAISS vector store locally at the given path
faiss_index.save_local(faiss_path)

# ✅ Inform the user that vector store creation was successful
print("✅ Vector store created at:", faiss_path)
