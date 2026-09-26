import sqlite3


# Name of our SQLite database file
DATABASE_NAME = "tasks.db"


# Connect to the database
connection = sqlite3.connect(DATABASE_NAME)


# Create a cursor
cursor = connection.cursor()


# SQL command to create the tasks table
create_table_sql = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


# Execute the SQL command
cursor.execute(create_table_sql)


# Save the changes
connection.commit()


# Close the database connection
connection.close()


print("Database and tasks table created successfully.")
