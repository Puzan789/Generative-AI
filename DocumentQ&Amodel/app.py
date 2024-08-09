import streamlit as st 
import os 
from langchain_groq import ChatGroq
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain # Create a chain for passing a list of Documents to a model.
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
from dotenv import load_dotenv
import time
load_dotenv()

## key laoding 
groq_api_key = os.getenv('GROQ_API_KEY') 
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY') 

st.title("Chat groQ with llama3")
llm=ChatGroq(groq_api_key=groq_api_key,
             model_name="Llama3-8b-8192")
prompt=ChatPromptTemplate.from_template(
    """
    Answer the  questions based on the provided context only. Please provide the most accurate response based on the question. 
    <context>
    {context}
    <context>        
    Questions:{input}                  
    """
)

def vector_embeddings():
    if "vectors" not in st.session_state:
        st.session_state.embeddings=GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        st.session_state.loader=PyPDFDirectoryLoader("./Uscensusdata")# Data ingestion technique
        st.session_state.docs=st.session_state.loader.load()# Document loading technique 
        st.session_state.text_splitters=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)# chunk creation 
        st.session_state.final_documents=st.session_state.text_splitters.split_documents(st.session_state.docs[:20])# splitting
        st.session_state.vector=FAISS.from_documents(st.session_state.final_documents,st.session_state.embeddings)# vector store
    


prompt1=st.text_input("Enter your questions from the document")

if st.button("Documents Embedding"):
    vector_embeddings()
    st.write("Vector store db is ready")



if prompt1:
    start=time.process_time()
    document_chain=create_stuff_documents_chain(llm,prompt)# responsiblefor returning the context
    retriever=st.session_state.vector.as_retriever()#Conversion: .as_retriever() converts this vector store into a retrieval system that can take a query (like a search term or question) and find the most relevant documents or chunks by comparing their vector representations.
    retrieval_chain=create_retrieval_chain(retriever,document_chain)#Purpose: The retrieval_chain combines the retriever with a document processing pipeline (document_chain) to create a structured workflow that can process and return the most relevant information.
    response=retrieval_chain.invoke({"input": prompt1})
    st.write(response['answer'])




