
## Features

- **Data Source**: Utilizes U.S. Census data, a comprehensive dataset that provides detailed demographic, economic, and housing information across the United States.
- **Document Embedding**: Embeds the U.S. Census documents using Google Generative AI embeddings.
- **Customizable Question-Answering**: Uses Groq's Llama3 model with a tailored prompt template to generate responses based on the provided U.S. Census data context.
- **Document Splitting**: Splits the U.S. Census documents into manageable chunks for efficient processing and retrieval.
- **Vector Store**: Stores and retrieves document vectors using FAISS for quick and accurate search results.

## Requirements

- Python 3.8 or above
- Streamlit
- LangChain
- Groq API key
- Google API key



## Usage

1. **Document Embedding**: Start by embedding the U.S. Census documents. Click the "Documents Embedding" button, and the app will process and store the document vectors.
2. **Ask Questions**: Enter your question in the text input field, and the system will retrieve the most relevant document chunks from the U.S. Census data and generate a precise answer.

## Key Components

- **U.S. Census Data**: The primary dataset used, which contains extensive information on U.S. demographics and economics.
- **Groq Llama3 Model**: The core language model used to generate answers based on the U.S. Census data.
- **Google Generative AI Embeddings**: Used to create vector embeddings for the U.S. Census documents, facilitating efficient retrieval.
- **FAISS**: A library used for efficient similarity search and clustering of dense vectors, critical for fast document retrieval.
- **Streamlit**: The web framework used to build and run the application, providing an interactive user interface.

## How It Works

1. **Document Loading**: PDF documents containing U.S. Census data are loaded from a specified directory.
2. **Text Splitting**: The U.S. Census documents are split into chunks using `RecursiveCharacterTextSplitter` to ensure they are manageable for processing.
3. **Vector Embeddings**: The text chunks from the U.S. Census documents are converted into vector embeddings using the Google Generative AI embeddings model.
4. **Vector Store**: The embeddings are stored in a FAISS index, enabling quick retrieval of relevant documents based on user queries.
5. **Question-Answering**: When a user inputs a question, the system retrieves the most relevant document chunks from the U.S. Census data and uses Groq's Llama3 model to generate an accurate and contextually appropriate answer.

