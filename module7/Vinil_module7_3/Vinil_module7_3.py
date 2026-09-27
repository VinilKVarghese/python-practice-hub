from fastapi import FastAPI
from datetime import datetime

app = FastAPI()


# Function to create server information
def get_server_information():
    # Get the current server time
    server_time = datetime.now()

    # Return server health and time
    return {
        "status": "healthy",
        "server_time": str(server_time)
    }


# POST API
@app.post("/server-info")
def server_info():
    # Get the server information
    information = get_server_information()

    # Return the information
    return information

