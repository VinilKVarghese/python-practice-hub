
import requests


def ask_ollama(user_text, system_prompt):
    """
    Sends the user's question and system prompt to Ollama.
    Returns the AI-generated response.
    """

    url = "http://localhost:11434/api/generate"

    data = {
        "model": "qwen2.5:1.5b",
        "system": system_prompt,
        "prompt": user_text,
        "stream": False
    }

    response = requests.post(url, json=data, timeout=120)

    response.raise_for_status()

    result = response.json()

    return result["response"]


# Define the AI's persona
system_prompt = (
    "You are a friendly Python teacher. "
    "Explain everything in simple words for beginners. "
    "Give examples whenever possible."
)

# Get the user's question
user_text = input("Enter your question: ")

try:
    # Call the function and store the response
    answer = ask_ollama(user_text, system_prompt)

    # Display the response
    print("\nAI Response:")
    print(answer)

except requests.exceptions.ConnectionError:
    print("Error: Ollama is not running. Please start Ollama.")

except requests.exceptions.Timeout:
    print("Error: Ollama took too long to respond.")

except requests.exceptions.RequestException as error:
    print(f"Error calling Ollama API: {error}")