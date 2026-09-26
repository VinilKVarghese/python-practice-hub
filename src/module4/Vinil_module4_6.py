
import sqlite3
import random
import string


# Name of the database
DATABASE_NAME = "tasks.db"


# Connect to the database
connection = sqlite3.connect(DATABASE_NAME)
cursor = connection.cursor()


# Add the new column to the tasks table
cursor.execute(
    "ALTER TABLE tasks ADD COLUMN missing_field TEXT"
)


# Get all existing task IDs
cursor.execute("SELECT id FROM tasks")
task_ids = cursor.fetchall()


# Populate the new column with one random character
for task in task_ids:

    # Generate one random character
    random_character = random.choice(string.ascii_letters)

    # Update the row with the random character
    cursor.execute(
        "UPDATE tasks SET missing_field = ? WHERE id = ?",
        (random_character, task[0])
    )


# Save the changes
connection.commit()


# Display the updated table
cursor.execute("SELECT * FROM tasks")
rows = cursor.fetchall()

print("Updated tasks table:")

for row in rows:
    print(row)


# Close the database connection
connection.close()