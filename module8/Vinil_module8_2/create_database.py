import sqlite3


def create_database():
    """Create a SQLite database and insert sample users."""

    # Connect to the database (creates it if it doesn't exist)
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    # Create the users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    """)

    # Insert sample data only if the table is empty
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]

    if count == 0:
        users = [
            ("Alvin", "0501234567"),
            ("Rahul", "0507654321"),
            ("Sara", "0509876543")
        ]

        cursor.executemany(
            "INSERT INTO users (name, phone) VALUES (?, ?)",
            users
        )

    # Save changes and close the connection
    connection.commit()
    connection.close()

    return "Database created successfully!"


# Call the function and display the result
result = create_database()
print(result)