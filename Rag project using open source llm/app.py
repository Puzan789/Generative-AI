import streamlit as st 
import os 
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.retrieval import create_retrieval_chain
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
import time
load_dotenv()

## Groq api key

groq_api_key=os.getenv('GROQ_API_KEY')
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
# Imagine you have an application where users can load a document from a URL and then perform some analysis on that document.
#  Without session state, each time the user performs an action (like clicking a button), the app would reset, and the document would need to be reloaded from the URL, which is inefficient.

if "vector" not in st.session_state:
    st.session_state.embeddings=GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    st.session_state.loader=WebBaseLoader("https://docs.smith.langchain.com/")
    st.session_state.docs=st.session_state.loader.load()
    st.session_state.text_splitters=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
    st.session_state.final_documents=st.session_state.text_splitters.split_documents(st.session_state.docs)
    st.session_state.vector=FAISS.from_documents(st.session_state.final_documents,st.session_state.embeddings)

st.title("ChatGroq")
llm=ChatGroq(groq_api_key=groq_api_key,model_name="mixtral-8x7b-32768")

prompt=ChatPromptTemplate.from_template(
"""
Answer the  questions based on the provided context only. Please provide the most accurate response based on the question. 
<context>
{context}
<context>        
Questions:{input}                  
""")
document_chain=create_stuff_documents_chain(llm,prompt)
retriever=st.session_state.vector.as_retriever()
retrieval_chain=create_retrieval_chain(retriever,document_chain)
prompt=st.text_input("Input your prompt here")

if prompt:
    start=time.process_time()
    response=retrieval_chain.invoke({"input":prompt})
    print("Response Time:",time.process_time()-start)
    st.write(response['answer'])

    with st.expander("Document Similarity Search"):
        for i ,doc in enumerate(response['context']):
            st.write(doc.page_content)
            st.write("_____________________--------------------------____________________")









