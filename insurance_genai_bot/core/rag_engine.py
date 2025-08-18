import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader, UnstructuredExcelLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from config.env import OPENAI_API_KEY, FAISS_DB_PATH


def build_faiss_index(pdf_files, excel_files):
    documents = []
    for pdf in pdf_files:
        docs = PyPDFLoader(pdf).load()
        documents.extend(docs)
    for xl in excel_files:
        docs = UnstructuredExcelLoader(xl).load()
        documents.extend(docs)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=80)
    split_docs = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    if not os.path.exists(FAISS_DB_PATH):
        faiss_index = FAISS.from_documents(split_docs, embeddings)
        faiss_index.save_local(FAISS_DB_PATH)
    else:
        faiss_index = FAISS.load_local(
            FAISS_DB_PATH, embeddings, allow_dangerous_deserialization=True
        )
    return faiss_index


def get_rag_chain():
    from config.env import DATA_FOLDER
    from utils.file_ops import list_data_files

    pdfs, excels = list_data_files(DATA_FOLDER)
    faiss_index = build_faiss_index(pdfs, excels)
    llm = ChatOpenAI(
        openai_api_key=OPENAI_API_KEY, model="gpt-3.5-turbo", temperature=0
    )
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=faiss_index.as_retriever(search_kwargs={"k": 5}),
        return_source_documents=True,
    )
    return qa_chain
