
import streamlit as st
import sqlite3
import requests


# -----------------------------------
# 1. SETTINGS
# -----------------------------------

DB_NAME = "chat_history.db"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:0.5b"


# -----------------------------------
# 2. CREATE DATABASE
# -----------------------------------

def create_database():
    """Create the database table if it does not exist."""

    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL
            )
        """)


# -----------------------------------
# 3. SAVE CHAT TO DATABASE
# -----------------------------------

def save_chat(question, answer):
    """Save the question and answer as text."""

    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            """
            INSERT INTO chat_history (question, answer)
            VALUES (?, ?)
            """,
            (question, answer)
        )


# -----------------------------------
# 4. LOAD CHAT HISTORY
# -----------------------------------

def load_chat_history():
    """Retrieve all saved chats from SQLite."""

    with sqlite3.connect(DB_NAME) as conn:
        rows = conn.execute(
            """
            SELECT id, question, answer
            FROM chat_history
            ORDER BY id
            """
        ).fetchall()

    return rows


# -----------------------------------
# 5. CLEAR CHAT HISTORY
# -----------------------------------

def clear_chat_history():
    """Delete all saved chat records."""

    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("DELETE FROM chat_history")


# -----------------------------------
# 6. CALL OLLAMA LLM
# -----------------------------------

def get_llm_response(question):
    """Send the user's question to Ollama."""

    payload = {
        "model": MODEL_NAME,
        "prompt": question,
        "stream": False
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120
        )

        response.raise_for_status()

        result = response.json()

        return result["response"]

    except requests.exceptions.RequestException as error:
        return f"Error connecting to Ollama: {error}"


# -----------------------------------
# 7. STREAMLIT UI
# -----------------------------------

def main():

    st.set_page_config(
        page_title="LLM Chatbot",
        page_icon="💬"
    )

    st.title("💬 My LLM Chatbot")
    st.write("Ask a question and get an answer from Ollama.")

    # Create the database table
    create_database()

    # -----------------------------------
    # CHAT INPUT
    # -----------------------------------

    question = st.chat_input("Type your question here...")

    if question:

        # Display the user's question
        with st.chat_message("user"):
            st.write(question)

        # Get the answer from Ollama
        with st.chat_message("assistant"):
            with st.spinner("Generating answer..."):
                answer = get_llm_response(question)

            st.write(answer)

        # Save question and answer to SQLite
        save_chat(question, answer)

    # -----------------------------------
    # DISPLAY SAVED CHAT HISTORY
    # -----------------------------------

    st.subheader("📜 Previous Chat History")

    history = load_chat_history()

    if history:
        for chat_id, saved_question, saved_answer in history:

            with st.expander(f"Chat {chat_id}: {saved_question}"):

                st.markdown("**Question:**")
                st.write(saved_question)

                st.markdown("**Answer:**")
                st.write(saved_answer)

    else:
        st.info("No chat history available yet.")

    # -----------------------------------
    # CLEAR HISTORY BUTTON
    # -----------------------------------

    if st.button("Clear Chat History"):
        clear_chat_history()
        st.rerun()


# -----------------------------------
# 8. RUN APPLICATION
# -----------------------------------

if __name__ == "__main__":
    main()