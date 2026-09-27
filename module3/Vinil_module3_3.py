from fastapi import FastAPI
from pydantic import BaseModel

# Create the FastAPI application
app = FastAPI()


# Create a model that describes the data we expect
class Message(BaseModel):
    # Text is required
    text: str


# Create a POST endpoint
@app.post("/message")
def create_message(message: Message):
    # Return the text that was received
    return {
        "message": message.text
    }