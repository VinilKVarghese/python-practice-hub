from fastapi import FastAPI
from datetime import datetime


# -------------------------------------------
# 1. Create the FastAPI application
# -------------------------------------------

app = FastAPI(
    title="Server Health API",
    description="API to check server health and current time"
)


# -------------------------------------------
# 2. Create the health endpoint
# -------------------------------------------

@app.get("/health")
def get_health():
    """
    Returns server health information
    and the current server time.
    """

    current_time = datetime.now().astimezone()

    return {
        "status": "healthy",
        "server": "FastAPI",
        "time": current_time.isoformat()
    }


# -------------------------------------------
# 3. Create the root endpoint
# -------------------------------------------

@app.get("/")
def home():
    """
    Returns a welcome message.
    """

    return {
        "message": "Welcome to the Server Health API",
        "health_endpoint": "/health"
    }