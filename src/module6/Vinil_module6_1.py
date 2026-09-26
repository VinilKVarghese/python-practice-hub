
from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate


# -----------------------------------
# CONFIGURATION
# -----------------------------------

DOCUMENT_PATH = "company_policy.docx"
DB_PATH = "./chroma_db"

CHAT_MODEL = "qwen2.5:0.5b"
EMBEDDING_MODEL = "nomic-embed-text"


# -----------------------------------
# STEP 1: LOAD THE WORD DOCUMENT
# -----------------------------------

def load_document(file_path):
    """
    Loads text from a Word .docx file.
    Returns a list of document objects.
    """

    loader = Docx2txtLoader(file_path)

    documents = loader.load()

    return documents


# -----------------------------------
# STEP 2: SPLIT DOCUMENT INTO CHUNKS
# -----------------------------------

def split_document(documents):
    """
    Splits document text into smaller chunks.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(documents)

    return chunks


# -----------------------------------
# STEP 3: CREATE EMBEDDINGS
# -----------------------------------

def create_embeddings():
    """
    Creates the embedding model used for
    converting text into vectors.
    """

    embeddings = OllamaEmbeddings(
        model=EMBEDDING_MODEL
    )

    return embeddings


# -----------------------------------
# STEP 4: STORE DOCUMENT IN CHROMA
# -----------------------------------

def store_documents(chunks, embeddings):
    """
    Stores document chunks and their embeddings
    in a persistent Chroma database.
    """

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="company_documents",
        persist_directory=DB_PATH
    )

    return vector_store


# -----------------------------------
# STEP 5: LOAD EXISTING VECTOR DATABASE
# -----------------------------------

def load_vector_store(embeddings):
    """
    Loads the existing Chroma database.
    """

    vector_store = Chroma(
        collection_name="company_documents",
        embedding_function=embeddings,
        persist_directory=DB_PATH
    )

    return vector_store


# -----------------------------------
# STEP 6: RETRIEVE TOP 3 CHUNKS
# -----------------------------------

def retrieve_documents(vector_store, user_question):
    """
    Retrieves the 3 most relevant document chunks.
    """

    results = vector_store.similarity_search(
        query=user_question,
        k=3
    )

    return results


# -----------------------------------
# STEP 7: GENERATE ANSWER USING OLLAMA
# -----------------------------------

def generate_answer(user_question, retrieved_documents):
    """
    Uses the retrieved document chunks as context
    and asks the LLM to answer the question.
    """

    llm = ChatOllama(
        model=CHAT_MODEL,
        temperature=0
    )

    context = "\n\n".join(
        document.page_content
        for document in retrieved_documents
    )

    prompt = ChatPromptTemplate.from_template(
        """
        You are a helpful assistant answering questions
        using the provided document context.

        Answer the question using only the information
        in the context.

        If the answer is not present in the context,
        say: "The document does not contain this information."

        Context:
        {context}

        Question:
        {question}

        Answer:
        """
    )

    messages = prompt.format_messages(
        context=context,
        question=user_question
    )

    response = llm.invoke(messages)

    return response.content


# -----------------------------------
# MAIN PROGRAM
# -----------------------------------

def main():

    # Load the document
    documents = load_document(DOCUMENT_PATH)

    print(f"Loaded {len(documents)} document(s).")

    # Split the document into chunks
    chunks = split_document(documents)

    print(f"Created {len(chunks)} chunks.")

    # Create embedding model
    embeddings = create_embeddings()

    # Store document chunks in Chroma
    vector_store = store_documents(chunks, embeddings)

    print("Document stored successfully.")

    # Get the user's question
    user_question = input("\nEnter your question: ")

    # Retrieve the top 3 relevant chunks
    retrieved_documents = retrieve_documents(
        vector_store,
        user_question
    )

    # Display the retrieved chunks
    print("\nTop 3 Retrieved Chunks:\n")

    for index, document in enumerate(retrieved_documents, start=1):
        print(f"--- Result {index} ---")
        print(document.page_content)
        print()

    # Generate the final answer
    answer = generate_answer(
        user_question,
        retrieved_documents
    )

    # Display the answer
    print("\nAI Answer:\n")
    print(answer)


# Run the program
if __name__ == "__main__":
    main()