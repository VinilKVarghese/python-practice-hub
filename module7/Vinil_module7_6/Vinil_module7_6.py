
import os
import requests
import streamlit as st


# Read environment variables
PERSONA_MODE = os.getenv("PERSONA_MODE", "false").lower() == "true"
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "qwen2.5:1.5b")


# Function to create the system prompt
def get_system_prompt(persona_mode):
    """Return a prompt based on the persona setting."""

    if persona_mode:
        return (
            "You are a friendly Python tutor. "
            "Explain concepts in simple language, "
            "use examples, and help beginners learn."
        )

    return "You are a helpful assistant."


# Function to send the chat messages to Ollama
def get_ollama_response(messages, persona_mode):
    """Send messages to Ollama and return its response."""

    system_prompt = get_system_prompt(persona_mode)

    # Add the system prompt before the conversation
    chat_messages = [
        {"role": "system", "content": system_prompt}
    ] + messages

    payload = {
        "model": MODEL_NAME,
        "messages": chat_messages,
        "stream": False
    }

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json=payload,
            timeout=300
        )

        response.raise_for_status()

        result = response.json()
        return result["message"]["content"]

    except requests.exceptions.RequestException as error:
        return f"Error connecting to Ollama: {error}"


# Streamlit page configuration
st.set_page_config(
    page_title="Ollama Chat",
    page_icon="💬",
    layout="centered"
)

st.title("💬 Chat with Ollama")

# Display the selected chat mode
if PERSONA_MODE:
    st.info("Chat mode: Python Tutor Persona")
else:
    st.info("Chat mode: Normal Assistant")


# Store conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Accept user input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Display and save the user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate and display the assistant response
    with st.chat_message("assistant"):
        with st.spinner("Ollama is thinking..."):
            response = get_ollama_response(
                st.session_state.messages,
                PERSONA_MODE
            )

        st.markdown(response)

    # Save the assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )


# Button to clear conversation history
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()