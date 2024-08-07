
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
from langchain_core.prompts  import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
import os
from dotenv import load_dotenv
import streamlit as st
load_dotenv()

os.environ['GOOGLE_API_KEY']=os.getenv("GOOGLE_API_KEY")
os.environ['LANGCHAIN_TRACING_V2'] = "true"
os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")

prompt=ChatPromptTemplate.from_messages([
    ("system", "you are a helpful assistant .Please response to the user queries "),
    ("user","Question:{question}")
])

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro-latest",
    temperature=0.6,
    safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    },)

# Streamlit
st.title("Langchain demo wit Google gen api")
input_text=st.text_input("Search the topic you want")

output_parser=StrOutputParser() # convert into string output format.
chain=prompt|llm|output_parser
if input_text:
    st.write(chain.invoke({'question':input_text}))
