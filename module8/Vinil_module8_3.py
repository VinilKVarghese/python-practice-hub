import requests
from mcp.server.fastmcp import FastMCP

# Create the MCP server
mcp = FastMCP("Ollama Question Answer Server")

# Ollama API URL
OLLAMA_URL = "http://localhost:11434/api/chat"

# Name of the Ollama model
MODEL_NAME = "qwen2.5:1.5b"


@mcp.tool()
def ask_ollama(question: str) -> str:
    """
    Send a user question to Ollama and return the answer.
    """

    # Check whether the question is empty
    if not question.strip():
        return "Error: Please enter a question."

    # Prepare the request data
    data = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ],
        "stream": False
    }

    try:
        # Send the question to Ollama
        response = requests.post(
            OLLAMA_URL,
            json=data,
            timeout=120
        )

        # Raise an error if the request failed
        response.raise_for_status()

        # Get the answer from Ollama
        result = response.json()
        answer = result["message"]["content"]

        return answer

    except requests.exceptions.RequestException as error:
        return f"Error connecting to Ollama: {error}"

    except (KeyError, ValueError):
        return "Error: Could not read the response from Ollama."


# Start the MCP server
if __name__ == "__main__":
    mcp.run(transport="stdio")