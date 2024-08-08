# LangChain Streamlit Application

This repository contains a Streamlit application that integrates several components from the LangChain library to perform document retrieval and question-answering based on a given document.

## Overview

The application allows users to load a document from a URL, split it into chunks, generate embeddings, store them in a vector store, and perform retrieval and question-answering using a language model. It uses Streamlit's session state to avoid reloading the document on every user interaction.

## Theoretical Concepts

### Environment Setup
Environment variables are loaded to securely manage API keys and configurations. This ensures that sensitive information is not hard-coded into the application.

### Streamlit Session State Initialization
Streamlit's session state is utilized to maintain the state of the application across user interactions. This prevents the need to reload and reprocess documents with every user action, thus enhancing efficiency.

### Document Loading and Splitting
Documents are loaded from a specified URL. These documents are then split into manageable chunks. This chunking process helps in efficient processing and embedding of the text data.

### Embedding Generation
Embeddings are generated for the document chunks. Embeddings are vector representations of text that capture the semantic meaning, allowing for efficient similarity searches and retrieval operations.

### Vector Store
The generated embeddings are stored in a FAISS (Facebook AI Similarity Search) vector store. This vector store enables fast and efficient similarity searches by organizing and indexing the embeddings.

### Language Model and Prompt Template
A language model (ChatGroq) is initialized to handle the natural language processing tasks. A prompt template is used to format the questions and context for the language model, ensuring consistent and accurate responses.

### Document and Retrieval Chains
Document chains and retrieval chains are created to manage the flow of information and processing steps. The document chain handles the integration of the language model with the prompt template, while the retrieval chain manages the retrieval of relevant documents based on user queries.

### User Interaction and Response Handling
The user provides input via a text prompt. The application processes this input using the retrieval chain, generating a response based on the most relevant document chunks. The response is then displayed to the user along with the retrieved documents for reference.

## Flowchart

```mermaid
flowchart TD
    A[Start] --> B[Load Environment Variables]
    B --> C{Check if "vector" in Session State}
    C -->|No| D[Initialize Embeddings and Load Document]
    D --> E[Split Document into Chunks]
    E --> F[Generate Embeddings for Document Chunks]
    F --> G[Store Embeddings in FAISS Vector Store]
    C -->|Yes| H[Retrieve Existing FAISS Vector Store]
    H --> I[Initialize Language Model]
    I --> J[Create Prompt Template]
    J --> K[Create Document Chain]
    K --> L[Create Retrieval Chain]
    L --> M[User Inputs Prompt]
    M --> N{Is Prompt Provided?}
    N -->|Yes| O[Invoke Retrieval Chain]
    O --> P[Display Response]
    O --> Q[Display Response Time]
    O --> R[Display Retrieved Documents]
    N -->|No| S[Wait for User Input]

    style A fill:#f9f,stroke:#333,stroke-width:4px
    style S fill:#ff9,stroke:#333,stroke-width:4px
    style P fill:#bbf,stroke:#333,stroke-width:4px
    style Q fill:#bbf,stroke:#333,stroke-width:4px
    style R fill:#bbf,stroke:#333,stroke-width:4px
