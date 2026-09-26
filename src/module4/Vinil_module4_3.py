from fastapi import FastAPI
import sqlite3


# Create the FastAPI application
app = FastAPI()


# Database file
DATABASE_NAME = "tasks.db"


# Create POST API
@app.post("/tasks")
def create_tasks():

    # Connect to the SQLite database
    connection = sqlite3.connect(DATABASE_NAME)

    # Create a cursor to execute SQL commands
    cursor = connection.cursor()

    # First task
    cursor.execute(
        """
        INSERT INTO tasks (title, description, status)
        VALUES (?, ?, ?)
        """,
        (
            "Learn Python",
            "Study Python basics",
            "pending"
        )
    )

    # Second task
    cursor.execute(
        """
        INSERT INTO tasks (title, description, status)
        VALUES (?, ?, ?)
        """,
        (
            "Learn FastAPI",
            "Build a simple FastAPI application",
            "pending"
        )
    )

    # Save the changes to the database
    connection.commit()

    # Close the database connection
    connection.close()

    # Return a response
    return {
        "message": "2 tasks inserted successfully"
    }
