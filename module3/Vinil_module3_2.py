from fastapi import FastAPI
from datetime import datetime

# Create the FastAPI application
app = FastAPI()


# Create a POST endpoint called /message
@app.post("/message")
def create_message():
    # Get the current date and time from the server
    server_time = datetime.now()

    # Return the message and server timestamp
    return {
        "message": "Hello from the server",
        "timestamp": server_time
    }