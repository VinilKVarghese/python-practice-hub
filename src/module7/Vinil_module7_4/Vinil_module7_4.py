
import sqlite3
import random
import secrets
import string
import os


# Function to generate random user data
def generate_random_user(user_id):
    """Generate random values for one user and return them."""

    names = [
        "Alvin", "John", "David", "Sarah",
        "Emma", "Michael", "Sophia", "Daniel"
    ]

    name = random.choice(names)

    # Generate a random 10-digit phone number
    phone = "05" + "".join(
        random.choices(string.digits, k=8)
    )

    # Generate a unique random user key
    user_key = secrets.token_hex(8)

    return {
        "id": user_id,
        "name": name,
        "phone": phone,
        "user_key": user_key
    }


# Function to create the database table
def create_table():
    """Create the users table if it does not exist."""
    os.makedirs("/app/data", exist_ok=True)
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            user_key TEXT NOT NULL UNIQUE
        )
    """)

    connection.commit()
    connection.close()


# Function to insert user data into the database
def insert_user(user):
    """Insert one user record into the SQL database."""

    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO users (id, name, phone, user_key)
        VALUES (?, ?, ?, ?)
    """, (
        user["id"],
        user["name"],
        user["phone"],
        user["user_key"]
    ))

    connection.commit()
    connection.close()


# Function to display all users stored in the database
def display_users():
    """Retrieve and display all user records."""

    connection = sqlite3.connect("/app/data/users.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    print("\nUsers stored in the database:")
    print("-" * 75)

    for row in rows:
        print(row)

    connection.close()


# Main program
if __name__ == "__main__":

    # Create the database table
    create_table()

    # Generate and store 10 random users
    for user_id in range(1, 11):
        user = generate_random_user(user_id)
        insert_user(user)

    # Display the stored records
    display_users()