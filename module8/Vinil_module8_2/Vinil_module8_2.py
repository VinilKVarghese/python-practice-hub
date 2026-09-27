import sqlite3
from mcp.server.fastmcp import FastMCP

# Create the MCP server
mcp = FastMCP("SQLite Database Server")

from pathlib import Path

# Get the folder where server.py is located
BASE_DIR = Path(__file__).resolve().parent

# Set the full database path
DATABASE_PATH = BASE_DIR / "users.db"

def connect_database():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE_PATH)


@mcp.tool()
def get_all_users() -> list:
    """Retrieve all users from the database."""

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("SELECT id, name, phone FROM users")
    rows = cursor.fetchall()

    connection.close()

    # Convert database rows into a list of dictionaries
    users = []

    for row in rows:
        users.append({
            "id": row[0],
            "name": row[1],
            "phone": row[2]
        })

    return users


@mcp.tool()
def get_user_by_id(user_id: int) -> dict:
    """Retrieve a user by their ID."""

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, name, phone FROM users WHERE id = ?",
        (user_id,)
    )

    row = cursor.fetchone()
    connection.close()

    if row is None:
        return {"error": "User not found"}

    return {
        "id": row[0],
        "name": row[1],
        "phone": row[2]
    }


@mcp.tool()
def get_total_users() -> int:
    """Return the total number of users in the database."""

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]

    connection.close()

    return count


# Start the MCP server using STDIO
if __name__ == "__main__":
    mcp.run(transport="stdio")