
import sqlite3
import time


# Name of the database
DATABASE_NAME = "Vinil_module4_2.db"


# ID of the task we want to change
task_id = 1


# Connect to the database
connection = sqlite3.connect(DATABASE_NAME)

# Create a cursor
cursor = connection.cursor()


# Get the original values of the task
cursor.execute(
    """
    SELECT title, description, status
    FROM tasks
    WHERE id = ?
    """,
    (task_id,)
)

original_task = cursor.fetchone()


# Check if the task exists
if original_task is None:
    print("Task not found.")

else:
    # Store the original values
    original_title = original_task[0]
    original_description = original_task[1]
    original_status = original_task[2]

    print("Original values:")
    print("Title:", original_title)
    print("Description:", original_description)
    print("Status:", original_status)


    # Change the task values
    cursor.execute(
        """
        UPDATE tasks
        SET title = ?,
            description = ?,
            status = ?
        WHERE id = ?
        """,
        (
            "Updated Task",
            "This task has been temporarily changed",
            "in_progress",
            task_id
        )
    )


    # Save the changes
    connection.commit()

    print("\nTask has been changed.")
    print("You have 15 seconds to check the SQL viewer.")


    # Wait for 15 seconds
    time.sleep(15)


    # Revert the task to its original values
    cursor.execute(
        """
        UPDATE tasks
        SET title = ?,
            description = ?,
            status = ?
        WHERE id = ?
        """,
        (
            original_title,
            original_description,
            original_status,
            task_id
        )
    )


    # Save the reverted values
    connection.commit()

    print("\nTask has been reverted.")
    print("The original values are restored.")


# Close the database connection
connection.close()

