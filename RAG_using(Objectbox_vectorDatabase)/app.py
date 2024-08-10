import os 
import streamlit as st 
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.retrieval import create_retrieval_chain
from dotenv import load_dotenv
from langchain_objectbox.vectorstores import ObjectBox
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFDirectoryLoader

# Load environment variables
load_dotenv()

# Set environment variables
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Title of the app
st.title("ObjectBox VectorStoreDb with Groq API")

# Initialize the language model
llm = ChatGroq(
    groq_api_key=os.getenv('GROQ_API_KEY'),
    model_name="Llama3-8b-8192"
)

# Define the prompt template
prompt = ChatPromptTemplate.from_template(
    """
    Answer the questions based on the provided context only. Please provide the most accurate response based on the question. 
    <context>
    {context}
    <context>
    Questions: {input}
    """
)

# Function to initialize vector embedding and ObjectBox VectorStore
def vector_embedding():
    if "vectors" not in st.session_state:
        # Load and process documents
        st.session_state.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        st.session_state.loader = PyPDFDirectoryLoader("./Uscensusdata")  # Data ingestion
        st.session_state.docs = st.session_state.loader.load()

        # Split documents
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs)

        # Initialize the ObjectBox vector store
        st.session_state.vectors = ObjectBox.from_documents(
            st.session_state.final_documents,
            st.session_state.embeddings,
            embedding_dimensions=512
        )

# Input field for user question
input_prompt = st.text_input("Enter your question from Documents")

# Button to trigger document embedding
if st.button("Documents Embedding"):
    vector_embedding()
    st.write("ObjectBox vector DB is ready")

# Handling the input prompt
if input_prompt:
    # Ensure that vectors are initialized before using them
    if "vectors" in st.session_state and st.session_state.vectors is not None:
        # Create the document chains and retrieval chain
        documents_chains = create_stuff_documents_chain(llm, prompt)
        retriever = st.session_state.vectors.as_retriever()
        retrieval_chain = create_retrieval_chain(retriever, documents_chains)

        # Get the response based on the user input
        response = retrieval_chain.invoke({"input": input_prompt})
        st.write(response['answer'])
    else:
        st.write("Please embed the documents first by clicking the 'Documents Embedding' button.")
