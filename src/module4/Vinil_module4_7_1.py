
import sqlite3


# Database name
DATABASE_NAME = "tasks.db"


# Approach 1: Sort using SQL ORDER BY
def sort_using_sql():

    # Connect to the database
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    # Sort rows using SQL
    cursor.execute(
        """
        SELECT *
        FROM tasks
        ORDER BY missing_field ASC
        """
    )

    # Get the sorted rows
    rows = cursor.fetchall()

    # Close the connection
    connection.close()

    return rows


# Approach 2: Sort using Python sorted()
def sort_using_python():

    # Connect to the database
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    # Get all rows from the table
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()

    # Sort rows using Python
    sorted_rows = sorted(
        rows,
        key=lambda row: row[-1]
    )

    # Close the connection
    connection.close()

    return sorted_rows


# Main program
if __name__ == "__main__":

    # Call 1: SQL sorting
    sql_result = sort_using_sql()

    print("\n--- Sorting using SQL ORDER BY ---")

    for row in sql_result:
        print(row)


    # Call 2: Python sorting
    python_result = sort_using_python()

    print("\n--- Sorting using Python sorted() ---")

    for row in python_result:
        print(row)