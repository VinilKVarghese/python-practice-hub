
import requests


def ask_ollama(user_text):
    """
    Sends the user's text to Ollama and returns the AI response.
    """

    url = "http://localhost:11434/api/generate"

    data = {
        "model": "qwen2.5:0.5b",
        "prompt": user_text,
        "stream": False
    }

    response = requests.post(url, json=data, timeout=120)

    response.raise_for_status()

    result = response.json()

    return result["response"]


# Get text input from the user
user_text = input("Enter your question: ")

try:
    # Call the function and store the AI's response
    answer = ask_ollama(user_text)

    # Display the response
    print("\nOllama's response:")
    print(answer)

except requests.exceptions.ConnectionError:
    print("Error: Ollama is not running. Please start Ollama.")

except requests.exceptions.Timeout:
    print("Error: Ollama took too long to respond.")

except requests.exceptions.RequestException as error:
    print(f"Error calling Ollama API: {error}")