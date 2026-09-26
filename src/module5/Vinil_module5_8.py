
import streamlit as st
import requests
import sqlite3


# -------------------------------
# DATABASE FUNCTIONS
# -------------------------------

DB_NAME = "chat_history.db"


def create_database():
    """
    Creates the database and messages table
    if they do not already exist.
    """

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_message(role, content):
    """
    Saves one message into the database.
    """

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO messages (role, content) VALUES (?, ?)",
        (role, content)
    )

    connection.commit()
    connection.close()


def load_messages():
    """
    Loads all saved messages in the correct order.
    Returns them as a list of dictionaries.
    """

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT role, content FROM messages ORDER BY id ASC"
    )

    rows = cursor.fetchall()
    connection.close()

    messages = []

    for role, content in rows:
        messages.append({
            "role": role,
            "content": content
        })

    return messages


def clear_messages():
    """
    Deletes all saved messages from the database.
    """

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM messages")

    connection.commit()
    connection.close()


# -------------------------------
# OLLAMA API FUNCTION
# -------------------------------

def chat_with_ollama(messages):
    """
    Sends the complete conversation history to Ollama
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


# -------------------------------
# STREAMLIT APPLICATION
# -------------------------------

# Create the database and table
create_database()

# Set the page title
st.title("Chat with Ollama")

st.write("Your chat history is saved and restored automatically.")

# Load saved messages when the session starts
if "messages" not in st.session_state:
    st.session_state.messages = load_messages()


# -------------------------------
# DISPLAY SAVED CHAT HISTORY
# -------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# -------------------------------
# CHAT INPUT
# -------------------------------

user_text = st.chat_input("Type your message here...")

if user_text:

    # Save the user's message in the database
    save_message("user", user_text)

    # Add the user's message to session state
    st.session_state.messages.append({
        "role": "user",
        "content": user_text
    })

    # Display the user's message
    with st.chat_message("user"):
        st.write(user_text)

    try:
        # Send the complete conversation history to Ollama
        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                answer = chat_with_ollama(
                    st.session_state.messages
                )

            st.write(answer)

        # Save the AI response in the database
        save_message("assistant", answer)

        # Add the AI response to session state
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


# -------------------------------
# CLEAR CHAT BUTTON
# -------------------------------

if st.button("Clear Chat"):

    # Delete all messages from the database
    clear_messages()

    # Clear messages from the current session
    st.session_state.messages = []

    # Refresh the page
    st.rerun()