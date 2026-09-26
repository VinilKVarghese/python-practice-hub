from fastapi import FastAPI
from pydantic import BaseModel

# Create the FastAPI application
app = FastAPI()


# Create a model that describes the person data
class Person(BaseModel):
    # Name is required and must be text
    name: str

    # Phone number is required and kept as text
    phone_number: str


# Create a POST endpoint
@app.post("/person")
def create_person(person: Person):
    # Return the person information
    return {
        "message": "Person created successfully",
        "name": person.name,
        "phone_number": person.phone_number
    }