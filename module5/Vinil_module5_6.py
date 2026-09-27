
import streamlit as st
import requests


def ask_ollama(user_text):
    """
    Sends the user's question to Ollama
    and returns the AI-generated response.
    """

    url = "http://localhost:11434/api/generate"

    data = {
        "model": "qwen2.5:1.5b",
        "prompt": user_text,
        "stream": False
    }

    response = requests.post(url, json=data, timeout=180)

    response.raise_for_status()

    result = response.json()

    return result["response"]


# Set the title of the web application
st.title("Ask Ollama")

# Display a short description
st.write("Enter your question and get an answer from AI.")

# Create a text input area for the user's question
user_text = st.text_area("Enter your question:")

# Create a button to submit the question
if st.button("Get Answer"):

    # Check whether the user entered a question
    if user_text.strip():

        try:
            # Show a loading message while Ollama generates an answer
            with st.spinner("Generating answer..."):

                # Call the function and store the result
                answer = ask_ollama(user_text)

            # Display the AI's response
            st.subheader("AI Response")
            st.write(answer)

        except requests.exceptions.ConnectionError:
            st.error("Ollama is not running. Please start Ollama.")

        except requests.exceptions.Timeout:
            st.error("Ollama took too long to respond.")

        except requests.exceptions.RequestException as error:
            st.error(f"Error calling Ollama API: {error}")

    else:
        st.warning("Please enter a question first.")