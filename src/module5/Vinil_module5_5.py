
import requests


def ask_ollama(user_text, context_size, temperature):
    """
    Sends the user's question to Ollama with a custom
    context window and temperature.

    Returns the AI-generated response.
    """

    url = "http://localhost:11434/api/generate"

    data = {
        "model": "qwen2.5:1.5b",
        "prompt": user_text,
        "stream": False,
        "options": {
            "num_ctx": context_size,
            "temperature": temperature
        }
    }

    response = requests.post(url, json=data, timeout=180)

    response.raise_for_status()

    result = response.json()

    return result["response"]


# Get inputs from the user
user_text = input("Enter your question: ")

try:
    context_size = int(
        input("Enter context window size (e.g. 8192): ")
    )

    temperature = float(
        input("Enter temperature (e.g. 0.7): ")
    )

    # Basic input validation
    if context_size <= 0:
        raise ValueError("Context size must be greater than 0.")

    if temperature < 0:
        raise ValueError("Temperature cannot be negative.")

    # Call the function and store the result
    answer = ask_ollama(user_text, context_size, temperature)

    # Display the response
    print("\nAI Response:")
    print(answer)

except ValueError as error:
    print(f"Invalid input: {error}")

except requests.exceptions.ConnectionError:
    print("Error: Ollama is not running. Please start Ollama.")

except requests.exceptions.Timeout:
    print("Error: Ollama took too long to respond.")

except requests.exceptions.RequestException as error:
    print(f"Error calling Ollama API: {error}")