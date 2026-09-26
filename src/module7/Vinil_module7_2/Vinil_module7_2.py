import streamlit as st
from langchain_ollama import ChatOllama


# ------------------------------------------------
# 1. Create the Ollama model
# ------------------------------------------------

llm = ChatOllama(
    model="qwen2.5:1.5b",
    base_url="http://ollama:11434",
    temperature=0
)


# ------------------------------------------------
# 2. Function to get a response from Ollama
# ------------------------------------------------

def get_response(user_question):
    """
    Sends the user's question to Ollama
    and returns the model's response.
    """

    response = llm.invoke(user_question)

    return response.content


# ------------------------------------------------
# 3. Streamlit user interface
# ------------------------------------------------

st.title("Qwen Chat Application")

st.write("Enter your question and get a response from Qwen.")


# Get user input
user_question = st.text_area(
    "Enter your question:",
    placeholder="Example: Explain what Python is."
)


# Process the question
if st.button("Submit"):

    if user_question.strip() == "":
        st.warning("Please enter a question.")

    else:
        try:
            with st.spinner("Qwen is generating a response..."):

                result = get_response(user_question)

            st.subheader("Response")
            st.write(result)

        except Exception as error:
            st.error(f"Error: {error}")