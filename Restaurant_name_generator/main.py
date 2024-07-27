import streamlit as st
import langchain_he

st.title("Restaurant name generator")

cuisine=st.sidebar.selectbox("Pick a cuisine" ,("Srilankan","Italian","Mexican","Nepali","Ethiopian","Hungarian"))



if cuisine:
    response=langchain_he.generate_names(cuisine)
    st.header(response['restaurant_name'].strip())
    st.write("** Menu Items **")
    menu_items=response['menu_items'].strip().split(",")
    for item in menu_items:
        st.write("-",item)

