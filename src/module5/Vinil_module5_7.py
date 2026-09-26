
import streamlit as st
import requests


def chat_with_ollama(messages):
    """
    Sends the full conversation history to Ollama
    and returns the assistant's response.
    """

    url = "http://localhost:11434/api/chat"

    data = {
        "model": "qwen2.5:0.5b",
        "messages": messages,
        "stream": False
    }

    response = requests.post(url, json=data, timeout=180)

    response.raise_for_status()

    result = response.json()

    return result["message"]["content"]


# Set the title of the application
st.title("Chat with Ollama")

st.write("Ask questions and the AI will remember this conversation.")

# Initialize chat history when the app starts
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])

# Create a chat input box
user_text = st.chat_input("Type your message here...")

# Process the user's message
if user_text:

    # Store the user's message in chat history
    st.session_state.messages.append({
        "role": "user",
        "content": user_text
    })

    # Display the user's message
    with st.chat_message("user"):
        st.write(user_text)

    try:
        # Send the entire conversation history to Ollama
        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                answer = chat_with_ollama(
                    st.session_state.messages
                )

            # Display the AI's response
            st.write(answer)

        # Store the AI's response in chat history
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

    except requests.exceptions.ConnectionError:
        st.error("Ollama is not running. Please start Ollama.")

    except requests.exceptions.Timeout:
        st.error("Ollama took too long to respond.")

    except requests.exceptions.RequestException as error:
        st.error(f"Error calling Ollama API: {error}")

# Add a button to clear the conversation
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()