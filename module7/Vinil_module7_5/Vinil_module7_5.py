
import sqlite3
import secrets
import os


# Database location inside the Docker container
DB_PATH = "/app/data/users.db"


# Function to create the database table
def create_table():
    """Create the users table if it does not exist."""

    os.makedirs("/app/data", exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            user_key TEXT NOT NULL UNIQUE
        )
    """)

    connection.commit()
    connection.close()


# Function to insert user information
def insert_user(name, phone):
    """Insert a new user and return the result."""

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    user_key = secrets.token_hex(8)

    try:
        cursor.execute("""
            INSERT INTO users (name, phone, user_key)
            VALUES (?, ?, ?)
        """, (name, phone, user_key))

        connection.commit()
        user_id = cursor.lastrowid

        return f"User added successfully! ID: {user_id}"

    except sqlite3.Error as error:
        return f"Database error: {error}"

    finally:
        connection.close()


# Function to display all saved users
def display_users():
    """Retrieve and display all records."""

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users ORDER BY id")
    rows = cursor.fetchall()

    print("\nUsers stored in the database:")
    print("-" * 75)

    for row in rows:
        print(row)

    connection.close()


# Main program
if __name__ == "__main__":

    # Create the table without deleting existing records
    create_table()

    while True:
        print("\n--- User Registration ---")

        name = input("Enter name (or type 'exit' to finish): ")

        if name.strip().lower() == "exit":
            break

        phone = input("Enter phone number: ")

        # Check that the inputs are not empty
        if not name.strip() or not phone.strip():
            print("Name and phone cannot be empty.")
            continue

        # Store the new user
        result = insert_user(name.strip(), phone.strip())
        print(result)

    # Display all saved users
    display_users()