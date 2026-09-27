import requests

url = "http://localhost:11434/api/tags"

try:
    response = requests.get(url, timeout=10)
    print("Status:", response.status_code)
    print("Response:", response.text)

except requests.exceptions.ConnectionError as error:
    print("Connection error:", error)

except requests.exceptions.Timeout:
    print("Connection timed out")