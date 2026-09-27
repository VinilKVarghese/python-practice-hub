
from datetime import datetime
import random

from mcp.server.fastmcp import FastMCP


# Create the MCP server
mcp = FastMCP("Date and Random Number Server")


# Tool 1: Get the current system date and time
@mcp.tool()
def get_system_date() -> str:
    """Return the current system date and time."""

    current_date = datetime.now().astimezone()

    return current_date.strftime("%Y-%m-%d %H:%M:%S %Z")


# Tool 2: Generate a random number
@mcp.tool()
def generate_random_number() -> int:
    """Generate a random integer between 1 and 100."""

    number = random.randint(1, 100)

    return number


# Start the MCP server
if __name__ == "__main__":
    mcp.run(transport="stdio")