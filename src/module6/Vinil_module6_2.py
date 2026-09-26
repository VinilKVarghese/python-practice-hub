
import os
import sqlite3
import streamlit as st

from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate


# --------------------------------------------------
# 1. SETTINGS
# --------------------------------------------------

DOCS_FOLDER = "docs"
DB_PATH = "chat_history.db"
CHROMA_PATH = "chroma_db"

LLM_MODEL = "qwen2.5:0.5b"
EMBEDDING_MODEL = "nomic-embed-text"

TOP_K = 3


# --------------------------------------------------
# 2. SQLITE CHAT MEMORY
# --------------------------------------------------

def create_database():
    """Create the chat history table if it does not exist."""

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL
            )
        """)


def save_message(role, content):
    """Save one message to SQLite."""

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO messages (role, content) VALUES (?, ?)",
            (role, content)
        )


def load_chat_history():
    """Load all previous messages from SQLite."""

    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            "SELECT role, content FROM messages ORDER BY id"
        ).fetchall()

    return [
        {"role": role, "content": content}
        for role, content in rows
    ]


def clear_chat_history():
    """Delete all saved chat messages."""

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM messages")


# --------------------------------------------------
# 3. LOAD DOCX FILES
# --------------------------------------------------

def load_documents(folder_path):
    """Load all Word documents from the docs folder."""

    documents = []

    if not os.path.exists(folder_path):
        raise FileNotFoundError(
            f"Folder '{folder_path}' does not exist."
        )

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".docx"):
            file_path = os.path.join(folder_path, filename)

            loader = Docx2txtLoader(file_path)
            docs = loader.load()

            # Keep the source filename in metadata
            for doc in docs:
                doc.metadata["source"] = filename

            documents.extend(docs)

    if not documents:
        raise ValueError(
            "No .docx files found in the docs folder."
        )

    return documents


# --------------------------------------------------
# 4. SPLIT DOCUMENTS INTO CHUNKS
# --------------------------------------------------

def split_documents(documents):
    """Split documents into smaller searchable chunks."""

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    return splitter.split_documents(documents)


# --------------------------------------------------
# 5. CREATE OR LOAD CHROMA VECTOR DATABASE
# --------------------------------------------------

@st.cache_resource
def get_vectorstore():
    """Load existing Chroma data or create it from documents."""

    embeddings = OllamaEmbeddings(
        model=EMBEDDING_MODEL
    )

    vectorstore = Chroma(
        collection_name="company_documents",
        embedding_function=embeddings,
        persist_directory=CHROMA_PATH
    )

    # Only ingest documents when the collection is empty
    if vectorstore._collection.count() == 0:
        documents = load_documents(DOCS_FOLDER)
        chunks = split_documents(documents)

        vectorstore.add_documents(chunks)

    return vectorstore


# --------------------------------------------------
# 6. RETRIEVE TOP 3 DOCUMENT CHUNKS
# --------------------------------------------------

def retrieve_documents(vectorstore, question):
    """Find the 3 most relevant document chunks."""

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": TOP_K}
    )

    return retriever.invoke(question)


# --------------------------------------------------
# 7. FORMAT CHAT HISTORY
# --------------------------------------------------

def format_chat_history(messages):
    """Convert previous messages into readable text."""

    if not messages:
        return "No previous conversation."

    history = []

    for message in messages:
        role = message["role"].capitalize()
        content = message["content"]

        history.append(f"{role}: {content}")

    return "\n".join(history)


# --------------------------------------------------
# 8. GENERATE ANSWER USING RAG + CHAT MEMORY
# --------------------------------------------------

def generate_answer(question, chat_history, vectorstore):
    """Answer a question using memory and retrieved documents."""

    # Retrieve top 3 relevant document chunks
    retrieved_docs = retrieve_documents(
        vectorstore,
        question
    )

    # Combine the retrieved chunks into one context
    context_parts = []

    for index, doc in enumerate(retrieved_docs, start=1):
        source = doc.metadata.get("source", "Unknown")
        context_parts.append(
            f"[Document {index}: {source}]\n{doc.page_content}"
        )

    context = "\n\n".join(context_parts)

    # Format previous conversation
    history_text = format_chat_history(chat_history)

    # Create the prompt
    prompt = ChatPromptTemplate.from_template("""
You are a helpful company policy assistant.

Answer the user's question using the document context below.

Rules:
- Use the retrieved documents as the source of policy facts.
- Do not invent policy details.
- If the documents do not contain the answer, say:
  "I could not find this information in the provided documents."
- Use the conversation history to understand follow-up questions.
- Do not treat previous assistant answers as verified policy facts.
- Keep the answer clear and concise.
- Mention the source filename when possible.

Conversation history:
{history}

Retrieved document context:
{context}

Current question:
{question}

Answer:
""")

    # Initialize the LLM
    llm = ChatOllama(
        model=LLM_MODEL,
        temperature=0
    )

    # Build the chain and get the answer
    chain = prompt | llm

    response = chain.invoke({
        "history": history_text,
        "context": context,
        "question": question
    })

    return response.content, retrieved_docs


# --------------------------------------------------
# 9. STREAMLIT CHAT INTERFACE
# --------------------------------------------------

def main():
    st.set_page_config(
        page_title="Company Policy Chatbot",
        page_icon="📚"
    )

    st.title("📚 Company Policy Chatbot")
    st.caption(
        "Ask questions about your company documents."
    )

    # Initialize SQLite
    create_database()

    # Load saved messages only once per session
    if "messages" not in st.session_state:
        st.session_state.messages = load_chat_history()

    # Load the document database
    try:
        with st.spinner("Loading company documents..."):
            vectorstore = get_vectorstore()

    except Exception as error:
        st.error(f"Could not load documents: {error}")
        st.stop()

    # Display existing chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Clear chat button
    if st.button("Clear Chat"):
        clear_chat_history()
        st.session_state.messages = []
        st.rerun()

    # Get user input
    question = st.chat_input("Ask a question about company policy...")

    if question:
        # Display and save the user question
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        save_message("user", question)

        with st.chat_message("user"):
            st.markdown(question)

        # Generate the answer using RAG and memory
        with st.chat_message("assistant"):
            with st.spinner("Searching documents and generating answer..."):
                try:
                    answer, retrieved_docs = generate_answer(
                        question,
                        st.session_state.messages[:-1],
                        vectorstore
                    )

                    st.markdown(answer)

                    # Display retrieved sources
                    with st.expander("View retrieved document chunks"):
                        for index, doc in enumerate(
                            retrieved_docs, start=1
                        ):
                            st.markdown(
                                f"**Chunk {index} — "
                                f"{doc.metadata.get('source', 'Unknown')}**"
                            )
                            st.write(doc.page_content)

                except Exception as error:
                    answer = f"An error occurred: {error}"
                    st.error(answer)

        # Save the assistant response
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

        save_message("assistant", answer)


# --------------------------------------------------
# 10. RUN THE APPLICATION
# --------------------------------------------------

if __name__ == "__main__":
    main()