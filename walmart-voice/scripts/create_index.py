import os
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from src.prompts.prompts import RAG_SEARCH_PROMPT_TEMPLATE
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

print("Loading Docs...")
loader = DirectoryLoader("./files")
docs = loader.load()

print("Splitting Docs...")
doc_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=200)
doc_chunks = doc_splitter.split_documents(docs)

print("Loading embedding model...")
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

print("Creating vector store...")
vectorstore = Chroma.from_documents(doc_chunks, embeddings, persist_directory="db")

# Semantic vector search
vectorstore_retreiver = vectorstore.as_retriever(search_kwargs={"k": 3})

# Keyword search
keyword_retriever = BM25Retriever.from_documents(doc_chunks)
keyword_retriever.k = 3

# Hybride search
ensemble_retriever = EnsembleRetriever(
    retrievers=[vectorstore_retreiver, keyword_retriever], weights=[0.3, 0.7]
)

prompt = ChatPromptTemplate.from_template(RAG_SEARCH_PROMPT_TEMPLATE)

llm = ChatGroq(model="llama3-70b-8192", api_key=os.getenv("GROQ_API_KEY"))

# build retrieval chain using LCEL
# this will take the user query and generate the answer
rag_chain = (
    {"context": ensemble_retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

query = "What are the prices of laptops?"
result = rag_chain.invoke(query)
print(result)
