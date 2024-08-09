from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
from langserve import add_routes 
import uvicorn
import os 
from dotenv import load_dotenv

load_dotenv ()
os.environ['GOOGLE_API_KEY'] =os.getenv('GOOGLE_API_KEY')
os.environ['LANGCHAIN_TRACING_V2'] = "true"
os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")

app=FastAPI(
    title='Langchain Server',
    version="1.0",
    description="APi server created using Google Gen ai"

)
add_routes(
    app,
    ChatGoogleGenerativeAI(
    model="gemini-1.5-pro-latest",
    temperature=0.6,
    safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }),
    path="/googlegenai"
  
)
model= ChatGoogleGenerativeAI(
    model="gemini-1.5-pro-latest",
    temperature=0.6,
    safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    },)
prompt1=ChatPromptTemplate.from_template("Write an essay about {topic} with 100 words.")
# promp2=ChatPromptTemplate.from_template("writa an poem{topic} with 100 words") # This is for the ollama because we use multiple routes.
add_routes(
    app,
    prompt1|model,
    path="/essay"
)

# add_routes(
#     app,
#     prompt|model,
#     path="/poem"
# )

if __name__ == "__main__":
    uvicorn.run(app, host="localhost",port=8000)