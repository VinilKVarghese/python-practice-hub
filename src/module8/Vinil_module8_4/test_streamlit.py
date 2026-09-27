import streamlit as st

st.title("LLM Database Assistant")

st.write("Streamlit is working!")

name = st.text_input("Enter your name")

if st.button("Submit"):
    st.write(f"Hello, {name}!")