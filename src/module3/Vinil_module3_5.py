from fastapi import FastAPI, Request
import logging

# Create the FastAPI application
app = FastAPI()


# Create a logger
logger = logging.getLogger("fastapi_logger")
logger.setLevel(logging.INFO)

# Create a file handler to save logs in my_file.log
file_handler = logging.FileHandler("my_file.log")

# Create a console handler to show logs in the terminal
console_handler = logging.StreamHandler()

# Define the format of each log message
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)

# Apply the format to both handlers
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add both handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)


# Middleware runs for every request
@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Send the request to the correct API endpoint
    response = await call_next(request)

    # Get request method, path, and response status
    method = request.method
    path = request.url.path
    status = response.status_code

    # Write the information to console and my_file.log
    logger.info(f"{method} {path} - Status: {status}")

    # Return the response to the user
    return response


# A simple test endpoint
@app.get("/hello")
def hello():
    return {"message": "Hello"}


# Another test endpoint
@app.post("/person")
def create_person():
    return {"message": "Person created"}