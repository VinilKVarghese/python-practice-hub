import requests
import streamlit as st
import json


# ==================================================
# SETTINGS
# ==================================================

# Ollama settings
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen2.5:1.5b"

# FastAPI settings
API_URL = "http://127.0.0.1:8000"


# ==================================================
# FUNCTION: ASK QWEN
# ==================================================

def ask_qwen(question):
    """
    Send a question to Qwen and return the answer.
    """

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ],
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    return data["message"]["content"]


# ==================================================
# FUNCTION: GET ALL USERS
# ==================================================

def get_all_users():
    """
    Get all users from FastAPI.
    """

    response = requests.get(
        f"{API_URL}/users",
        timeout=10
    )

    response.raise_for_status()

    return response.json()


# ==================================================
# FUNCTION: SEARCH USERS
# ==================================================

def search_users(name):
    """
    Search users by name.
    """

    response = requests.get(
        f"{API_URL}/users/search",
        params={
            "name": name
        },
        timeout=10
    )

    response.raise_for_status()

    return response.json()


# ==================================================
# FUNCTION: ADD USER
# ==================================================

def add_user(name, age, city):
    """
    Add a new user to the database.
    """

    response = requests.post(
        f"{API_URL}/users",
        params={
            "name": name,
            "age": age,
            "city": city
        },
        timeout=10
    )

    response.raise_for_status()

    return response.json()


# ==================================================
# FUNCTION: UNDERSTAND QUESTION
# ==================================================

def understand_question(question):
    """
    Ask Qwen to identify the database operation.
    """

    prompt = f"""
You are a database assistant.

Return ONLY ONE of these words:

SHOW
SEARCH
ADD
OLDEST
YOUNGEST
COUNT
AVERAGE
OLDEST_AGE
YOUNGEST_AGE
CITY_SEARCH
OLDER_THAN
YOUNGER_THAN
CITY_COUNT
OTHER

Rules:

SHOW = show all users

SEARCH = find a user by name

ADD = add a new user

OLDEST = find the oldest user

YOUNGEST = find the youngest user

COUNT = count all users

AVERAGE = calculate average age

OLDEST_AGE = find highest age

YOUNGEST_AGE = find lowest age

CITY_SEARCH = find users in a city

OLDER_THAN = find users older than an age

YOUNGER_THAN = find users younger than an age

CITY_COUNT = count users in a city

OTHER = anything else

Examples:

Show all users -> SHOW

Find Jake -> SEARCH

Add Jake age 45 from Sharjah -> ADD

Who is the oldest user? -> OLDEST

Who is the youngest user? -> YOUNGEST

How many users are there? -> COUNT

What is the average age? -> AVERAGE

Who lives in Dubai? -> CITY_SEARCH

How many users live in Dubai? -> CITY_COUNT

Who is older than 40? -> OLDER_THAN

Who is younger than 30? -> YOUNGER_THAN

User question:
{question}
"""

    result = ask_qwen(prompt)

    result = result.strip().upper()

    # Check specific operations first
    if "YOUNGEST_AGE" in result:
        return "YOUNGEST_AGE"

    if "OLDEST_AGE" in result:
        return "OLDEST_AGE"

    if "CITY_COUNT" in result:
        return "CITY_COUNT"

    if "CITY_SEARCH" in result:
        return "CITY_SEARCH"

    if "OLDER_THAN" in result:
        return "OLDER_THAN"

    if "YOUNGER_THAN" in result:
        return "YOUNGER_THAN"

    if "YOUNGEST" in result:
        return "YOUNGEST"

    if "OLDEST" in result:
        return "OLDEST"

    if "AVERAGE" in result:
        return "AVERAGE"

    if "COUNT" in result:
        return "COUNT"

    if "SHOW" in result:
        return "SHOW"

    if "SEARCH" in result:
        return "SEARCH"

    if "ADD" in result:
        return "ADD"

    return "OTHER"


# ==================================================
# FUNCTION: EXTRACT USER INFORMATION
# ==================================================

def extract_user_information(question):
    """
    Ask Qwen to extract name, age and city
    from the user's sentence.
    """

    prompt = f"""
Extract user information from this sentence.

Return ONLY valid JSON.

The JSON must have exactly these fields:

{{
    "name": "",
    "age": null,
    "city": ""
}}

Rules:

- name = person's name
- age = person's age as a number
- city = person's city
- If something is missing, use null or an empty string.

Example:

Input:
Add user Jake having age 45 living in Sharjah

Output:
{{"name": "Jake", "age": 45, "city": "Sharjah"}}

Another example:

Input:
Add Sara, she is 25 and lives in Dubai

Output:
{{"name": "Sara", "age": 25, "city": "Dubai"}}

User sentence:
{question}
"""

    result = ask_qwen(prompt)

    # Remove possible markdown code fences
    result = result.replace("```json", "")
    result = result.replace("```", "")
    result = result.strip()

    try:

        data = json.loads(result)

        return data

    except json.JSONDecodeError:

        return {
            "name": "",
            "age": None,
            "city": ""
        }


# ==================================================
# FUNCTION: EXTRACT CITY
# ==================================================

def extract_city(question):
    """
    Ask Qwen to extract a city from the question.
    """

    prompt = f"""
Find the city mentioned in this question.

Return ONLY the city name.
Do not provide an explanation.

Question:
{question}
"""

    city = ask_qwen(prompt)

    return city.strip()


# ==================================================
# FUNCTION: EXTRACT AGE
# ==================================================

def extract_age(question):
    """
    Ask Qwen to extract an age from the question.

    Example:
    Who is older than 35?
    returns 35
    """

    prompt = f"""
Find the age number mentioned in this question.

Return ONLY the number.

Question:
{question}
"""

    result = ask_qwen(prompt)

    try:

        return int(result.strip())

    except ValueError:

        return None


# ==================================================
# FUNCTION: FIND OLDEST USER
# ==================================================

def find_oldest_user(users):
    """
    Find the user with the highest age.
    """

    if not users:
        return None

    oldest_user = users[0]

    for user in users:

        if user["age"] > oldest_user["age"]:

            oldest_user = user

    return oldest_user


# ==================================================
# FUNCTION: FIND YOUNGEST USER
# ==================================================

def find_youngest_user(users):
    """
    Find the user with the lowest age.
    """

    if not users:
        return None

    youngest_user = users[0]

    for user in users:

        if user["age"] < youngest_user["age"]:

            youngest_user = user

    return youngest_user


# ==================================================
# FUNCTION: CALCULATE AVERAGE AGE
# ==================================================

def calculate_average_age(users):
    """
    Calculate the average age.
    """

    if not users:
        return None

    total_age = 0

    for user in users:

        total_age += user["age"]

    return total_age / len(users)


# ==================================================
# FUNCTION: FIND USERS BY CITY
# ==================================================

def find_users_by_city(users, city):
    """
    Find users who live in a specific city.
    """

    matching_users = []

    for user in users:

        if user["city"].lower() == city.lower():

            matching_users.append(user)

    return matching_users


# ==================================================
# FUNCTION: FIND USERS OLDER THAN AGE
# ==================================================

def find_users_older_than(users, age):
    """
    Find users older than the specified age.
    """

    matching_users = []

    for user in users:

        if user["age"] > age:

            matching_users.append(user)

    return matching_users


# ==================================================
# FUNCTION: FIND USERS YOUNGER THAN AGE
# ==================================================

def find_users_younger_than(users, age):
    """
    Find users younger than the specified age.
    """

    matching_users = []

    for user in users:

        if user["age"] < age:

            matching_users.append(user)

    return matching_users


# ==================================================
# FUNCTION: COUNT USERS IN CITY
# ==================================================

def count_users_in_city(users, city):
    """
    Count users who live in a city.
    """

    count = 0

    for user in users:

        if user["city"].lower() == city.lower():

            count += 1

    return count


# ==================================================
# STREAMLIT UI
# ==================================================

st.title("🤖 LLM Database Assistant")

st.write(
    "Ask questions about users stored in the SQL database."
)

st.write(
    "Database columns: ID, Name, Age and City."
)


# ==================================================
# USER QUESTION
# ==================================================

question = st.text_input(
    "Enter your question:"
)


# ==================================================
# ASK BUTTON
# ==================================================

if st.button("Ask"):

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        try:

            # Ask Qwen what the user wants
            operation = understand_question(question)

            st.write(
                "Detected operation:",
                operation
            )


            # ==================================================
            # SHOW ALL USERS
            # ==================================================

            if operation == "SHOW":

                users = get_all_users()

                if users:

                    st.subheader("All Users")

                    st.dataframe(users)

                else:

                    st.info(
                        "No users found."
                    )


            # ==================================================
            # SEARCH USER
            # ==================================================

            elif operation == "SEARCH":

                search_name = question

                # Ask Qwen for the person's name
                prompt = f"""
Extract only the person's name from this request.

Return ONLY the name.

Request:
{question}
"""

                search_name = ask_qwen(prompt).strip()

                users = search_users(search_name)

                if users:

                    st.subheader(
                        "Search Results"
                    )

                    st.dataframe(users)

                else:

                    st.info(
                        f"No user found with the name {search_name}."
                    )


            # ==================================================
            # ADD USER
            # ==================================================

            elif operation == "ADD":

                # Extract name, age and city
                user_data = extract_user_information(
                    question
                )

                name = user_data.get(
                    "name",
                    ""
                )

                age = user_data.get(
                    "age"
                )

                city = user_data.get(
                    "city",
                    ""
                )

                # Check that all information was found
                if not name or age is None or not city:

                    st.warning(
                        "I could not extract the name, age and city."
                    )

                    st.write(
                        "Please try something like:"
                    )

                    st.code(
                        "Add user Jake having age 45 living in Sharjah"
                    )

                else:

                    # Add the user to the database
                    result = add_user(
                        name,
                        age,
                        city
                    )

                    st.success(
                        "User added successfully!"
                    )

                    st.json(result)


            # ==================================================
            # OLDEST USER
            # ==================================================

            elif operation == "OLDEST":

                users = get_all_users()

                oldest_user = find_oldest_user(
                    users
                )

                if oldest_user:

                    st.subheader(
                        "Oldest User"
                    )

                    st.write(
                        f"The oldest user is "
                        f"**{oldest_user['name']}**, "
                        f"who is **{oldest_user['age']} years old** "
                        f"and lives in **{oldest_user['city']}**."
                    )

                else:

                    st.info(
                        "No users found."
                    )


            # ==================================================
            # YOUNGEST USER
            # ==================================================

            elif operation == "YOUNGEST":

                users = get_all_users()

                youngest_user = find_youngest_user(
                    users
                )

                if youngest_user:

                    st.subheader(
                        "Youngest User"
                    )

                    st.write(
                        f"The youngest user is "
                        f"**{youngest_user['name']}**, "
                        f"who is **{youngest_user['age']} years old** "
                        f"and lives in **{youngest_user['city']}**."
                    )

                else:

                    st.info(
                        "No users found."
                    )


            # ==================================================
            # COUNT USERS
            # ==================================================

            elif operation == "COUNT":

                users = get_all_users()

                count = len(users)

                st.write(
                    f"There are **{count} users** "
                    f"in the database."
                )


            # ==================================================
            # AVERAGE AGE
            # ==================================================

            elif operation == "AVERAGE":

                users = get_all_users()

                average_age = calculate_average_age(
                    users
                )

                if average_age is not None:

                    st.write(
                        f"The average age is "
                        f"**{average_age:.2f} years**."
                    )

                else:

                    st.info(
                        "No users found."
                    )


            # ==================================================
            # OLDEST AGE
            # ==================================================

            elif operation == "OLDEST_AGE":

                users = get_all_users()

                if users:

                    oldest_user = find_oldest_user(
                        users
                    )

                    st.write(
                        f"The highest age is "
                        f"**{oldest_user['age']} years**."
                    )

                else:

                    st.info(
                        "No users found."
                    )


            # ==================================================
            # YOUNGEST AGE
            # ==================================================

            elif operation == "YOUNGEST_AGE":

                users = get_all_users()

                if users:

                    youngest_user = find_youngest_user(
                        users
                    )

                    st.write(
                        f"The lowest age is "
                        f"**{youngest_user['age']} years**."
                    )

                else:

                    st.info(
                        "No users found."
                    )


            # ==================================================
            # CITY SEARCH
            # ==================================================

            elif operation == "CITY_SEARCH":

                # Extract the city from the question
                city = extract_city(question)

                users = get_all_users()

                matching_users = find_users_by_city(
                    users,
                    city
                )

                if matching_users:

                    st.subheader(
                        f"Users in {city}"
                    )

                    st.dataframe(
                        matching_users
                    )

                else:

                    st.info(
                        f"No users found in {city}."
                    )


            # ==================================================
            # OLDER THAN
            # ==================================================

            elif operation == "OLDER_THAN":

                age = extract_age(question)

                if age is None:

                    st.warning(
                        "I could not find an age in your question."
                    )

                else:

                    users = get_all_users()

                    matching_users = find_users_older_than(
                        users,
                        age
                    )

                    if matching_users:

                        st.subheader(
                            f"Users older than {age}"
                        )

                        st.dataframe(
                            matching_users
                        )

                    else:

                        st.info(
                            f"No users are older than {age}."
                        )


            # ==================================================
            # YOUNGER THAN
            # ==================================================

            elif operation == "YOUNGER_THAN":

                age = extract_age(question)

                if age is None:

                    st.warning(
                        "I could not find an age in your question."
                    )

                else:

                    users = get_all_users()

                    matching_users = find_users_younger_than(
                        users,
                        age
                    )

                    if matching_users:

                        st.subheader(
                            f"Users younger than {age}"
                        )

                        st.dataframe(
                            matching_users
                        )

                    else:

                        st.info(
                            f"No users are younger than {age}."
                        )


            # ==================================================
            # CITY COUNT
            # ==================================================

            elif operation == "CITY_COUNT":

                city = extract_city(question)

                users = get_all_users()

                count = count_users_in_city(
                    users,
                    city
                )

                st.write(
                    f"There are **{count} users** "
                    f"in **{city}**."
                )


            # ==================================================
            # OTHER QUESTIONS
            # ==================================================

            else:

                answer = ask_qwen(
                    question
                )

                st.subheader(
                    "Qwen"
                )

                st.write(
                    answer
                )


        except Exception as error:

            st.error(
                f"Error: {error}"
            )