import sqlite3


# Name of the SQLite database
DATABASE_NAME = "Vinil_module4_2.db"


# Connect to the database
connection = sqlite3.connect(DATABASE_NAME)

# Create a cursor
cursor = connection.cursor()


# Get all table names from the database
cursor.execute(
    """
    SELECT name
    FROM sqlite_master
    WHERE type = 'table';
    """
)

tables = cursor.fetchall()


# Display the table names
print("Tables in the database:")

for table in tables:
    print(table[0])


# Check if the tasks table exists
if ("tasks",) in tables:

    # Get all rows from the tasks table
    cursor.execute("SELECT * FROM tasks")

    rows = cursor.fetchall()

    print("\nData in tasks table:")

    # Display each row
    for row in rows:
        print(row)


# Close the database connection
connection.close()

