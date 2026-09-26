import streamlit as st
import sqlite3

from typing import Optional
from pydantic import BaseModel, model_validator

from langchain_ollama import ChatOllama


# =========================================================
# 1. Pydantic model
# =========================================================

class UserInformation(BaseModel):
    """
    Stores the information extracted from the user's input.
    At least one field must be provided.
    """

    name: Optional[str] = None
    time: Optional[str] = None
    number: Optional[int] = None

    @model_validator(mode="after")
    def check_at_least_one_field(self):
        """
        Make sure that at least one of name, time or number
        is provided.
        """

        if (
            self.name is None
            and self.time is None
            and self.number is None
        ):
            raise ValueError(
                "At least one of name, time or number is required."
            )

        return self


# =========================================================
# 2. Create Qwen model
# =========================================================

llm = ChatOllama(
    model="qwen2.5:7b",
    temperature=0
)


# =========================================================
# 3. Create structured output model
# =========================================================

structured_llm = llm.with_structured_output(UserInformation)


# =========================================================
# 4. Function to extract information using Qwen
# =========================================================

def extract_information(user_input):
    """
    Sends the user's input to Qwen and extracts
    name, time and number using the Pydantic model.
    """

    prompt = f"""
    Extract information from the following user input.

    We need these three fields:

    1. name - person's name
    2. time - time mentioned by the user
    3. number - numerical value mentioned by the user

    At least one field must be present.

    If a field is not provided, leave it empty.

    User input:
    {user_input}
    """

    result = structured_llm.invoke(prompt)

    return result


# =========================================================
# 5. Create SQLite database
# =========================================================

def create_database():
    """
    Creates the SQLite database and table if they
    do not already exist.
    """

    connection = sqlite3.connect("user_information.db")

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user_information (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            time TEXT,
            number INTEGER
        )
        """
    )

    connection.commit()
    connection.close()


# =========================================================
# 6. Store information in SQLite
# =========================================================

def save_to_database(user_information):
    """
    Saves the validated Pydantic data into SQLite.
    """

    connection = sqlite3.connect("user_information.db")

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO user_information
        (name, time, number)
        VALUES (?, ?, ?)
        """,
        (
            user_information.name,
            user_information.time,
            user_information.number
        )
    )

    connection.commit()
    connection.close()


# =========================================================
# 7. Get records from database
# =========================================================

def get_database_records():
    """
    Retrieves all saved records from the database.
    """

    connection = sqlite3.connect("user_information.db")

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, name, time, number
        FROM user_information
        """
    )

    records = cursor.fetchall()

    connection.close()

    return records


# =========================================================
# 8. Create database
# =========================================================

create_database()


# =========================================================
# 9. Streamlit UI
# =========================================================

st.title("🤖 Qwen Information Extractor")

st.write(
    "Enter information in natural language. "
    "Qwen will extract the name, time and number."
)


# ---------------------------------------------------------
# User input
# ---------------------------------------------------------

user_input = st.text_area(
    "Enter your information:",
    placeholder=(
        "Example: My name is John. "
        "My appointment is at 3 PM and my number is 25."
    )
)


# ---------------------------------------------------------
# Process button
# ---------------------------------------------------------

if st.button("Process Information"):

    if user_input.strip() == "":
        st.warning("Please enter some information.")

    else:

        try:

            # ---------------------------------------------
            # Send input to Qwen
            # ---------------------------------------------

            with st.spinner("Qwen is processing your input..."):

                result = extract_information(user_input)


            # ---------------------------------------------
            # Display Pydantic result
            # ---------------------------------------------

            st.subheader("Extracted Information")

            st.write("Name:", result.name)
            st.write("Time:", result.time)
            st.write("Number:", result.number)


            # ---------------------------------------------
            # Save to database
            # ---------------------------------------------

            save_to_database(result)

            st.success("Information successfully saved to database!")


        except Exception as error:

            st.error(
                f"Could not process the information: {error}"
            )


# =========================================================
# 10. Display saved records
# =========================================================

st.subheader("Saved Information")

records = get_database_records()

if records:

    for record in records:

        st.write(
            f"ID: {record[0]} | "
            f"Name: {record[1]} | "
            f"Time: {record[2]} | "
            f"Number: {record[3]}"
        )

else:

    st.info("No information has been saved yet.")