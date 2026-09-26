
import sqlite3
import os


# Name of the database
DATABASE_NAME = "tasks.db"


# Show the folder where Python is running
print("Python is running from:")
print(os.getcwd())


# Show the full path of the database
database_path = os.path.abspath(DATABASE_NAME)

print("\nDatabase being opened:")
print(database_path)


# Check whether the database file exists
if os.path.exists(database_path):
    print("\nDatabase file exists.")
else:
    print("\nDatabase file DOES NOT exist.")


# Connect to the database
connection = sqlite3.connect(DATABASE_NAME)

cursor = connection.cursor()


# Get all tables
cursor.execute(
    """
    SELECT name
    FROM sqlite_master
    WHERE type = 'table';
    """
)

tables = cursor.fetchall()


print("\nTables in the database:")

if tables:
    for table in tables:
        print(table[0])
else:
    print("No tables found.")


# Close connection
connection.close()

