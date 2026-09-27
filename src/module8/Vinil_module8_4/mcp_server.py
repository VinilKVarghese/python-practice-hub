import requests
from mcp.server.fastmcp import FastMCP

# Create MCP server
mcp = FastMCP("User Database MCP Server")

# FastAPI URL
API_URL = "http://127.0.0.1:8000"


@mcp.tool()
def add_user(name: str, age: int, city: str) -> dict:
    """
    Add a new user to the SQL database.
    """

    try:
        response = requests.post(
            f"{API_URL}/users",
            params={
                "name": name,
                "age": age,
                "city": city
            },
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as error:
        return {
            "error": f"Could not connect to database API: {error}"
        }


@mcp.tool()
def get_all_users() -> list:
    """
    Get all users from the SQL database.
    """

    try:
        response = requests.get(
            f"{API_URL}/users",
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as error:
        return [{
            "error": f"Could not connect to database API: {error}"
        }]


@mcp.tool()
def search_users(name: str) -> list:
    """
    Search for users by name.
    """

    try:
        response = requests.get(
            f"{API_URL}/users/search",
            params={"name": name},
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as error:
        return [{
            "error": f"Could not connect to database API: {error}"
        }]


# Start MCP server
if __name__ == "__main__":
    mcp.run(transport="stdio")