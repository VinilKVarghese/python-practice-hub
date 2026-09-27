import requests


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen2.5:1.5b"


def ask_qwen(question):
    """
    Send a question to Qwen and return its response.
    """

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ],
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    return data["message"]["content"]


# Get input from the user
question = input("Ask Qwen: ")

# Call the function
result = ask_qwen(question)

# Display the result
print("\nQwen says:")
print(result)