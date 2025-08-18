# LangChain RetrievalQA setup

import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set up LLM and embeddings
def get_rag_chain(db_path: str = None) -> RetrievalQA:
    
    # ✅ Hybrid - Load from env if not provided (Best for both dev and production)
    db_path = db_path or os.getenv("FAISS_DB_PATH", "vectordb/packers_faiss")

    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectorstore = FAISS.load_local(
        db_path,
        embeddings,
        allow_dangerous_deserialization=True
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    llm = ChatOpenAI(temperature=0.3, openai_api_key=OPENAI_API_KEY)
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type="stuff")
