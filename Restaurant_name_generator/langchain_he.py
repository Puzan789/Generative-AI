from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
from langchain.prompts import PromptTemplate
from langchain.chains import  SequentialChain,LLMChain
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")


def generate_names(cuisine):
    # Sequential chain
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=1,
        google_api_key=api_key,
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        },)
    prompt_template_name = PromptTemplate(input_variables=['cuisine'],
                                          template="I want to open a restaurant for  a {cuisine}. Suggest a restaurant name only dont gove more contain")
    name_chain = LLMChain(
        llm=llm, prompt=prompt_template_name, output_key='restaurant_name')
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=1,
        google_api_key=api_key,
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        },)
    prompt_template_items = PromptTemplate(
        input_variables=['restaurant_name'],
        template="suggest some menu items for {restaurant_name}. Return it as a comma seperated"
    )

    food_items_chain = LLMChain(
        llm=llm, prompt=prompt_template_items, output_key="menu_items")

    chain = SequentialChain(
        chains=[name_chain, food_items_chain],
        input_variables=["cuisine"],
        output_variables=["restaurant_name", 'menu_items']
    )
    response = chain.invoke({'cuisine': cuisine})
    return response
