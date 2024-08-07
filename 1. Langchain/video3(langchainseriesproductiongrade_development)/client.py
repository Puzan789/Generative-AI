import streamlit as st 
import requests

def get_google_api_response(input_text):
    response=requests.post("http://localhost:8000/essay/invoke",json={"input":{'topic':input_text}})
    return response.json()['output']['content']


st.title("Content creator web app with api")
input_text =st.text_input("write an essay o")

if input_text:
    st.write(get_google_api_response(input_text))
