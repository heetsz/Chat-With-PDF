import os
from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

# ✅ FREE LOCAL EMBEDDINGS
from langchain_community.embeddings import HuggingFaceEmbeddings

# ✅ GEMINI LLM (ONLY FOR CHAT)
from langchain_google_genai import ChatGoogleGenerativeAI


def load_pdf(pdf_path: str):
    loader = PyPDFLoader(pdf_path)
    return loader.load()


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )
    return splitter.split_documents(documents)


def get_embeddings():
    # 🔥 FREE – NO QUOTA
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def create_vector_store(chunks, embeddings):
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local("faiss_index")
    return vectorstore


def process_pdf(filename: str):
    pdf_path = os.path.join("uploads", filename)

    documents = load_pdf(pdf_path)
    chunks = split_documents(documents)
    embeddings = get_embeddings()

    create_vector_store(chunks, embeddings)
    return "PDF processed successfully"


def load_vector_store():
    embeddings = get_embeddings()
    return FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )


def chat_with_pdf(question: str):
    vectorstore = load_vector_store()

    docs = vectorstore.similarity_search(question, k=4)

    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = f"""
You are an assistant answering questions strictly from the given context, IF CONTEXT IS NOT VERY HELPFULL THEN CAN USE UR BRAIN.

Context:
{context}

Question:
{question}
"""

    # ✅ GEMINI USED ONLY HERE (LOW USAGE)
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0
    )

    response = llm.invoke(prompt)
    return response.content
