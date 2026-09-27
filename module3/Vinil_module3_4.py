from fastapi import FastAPI
import random

app = FastAPI()

# Variable to store the person's details
person_data = {}


# Function to accept and return person details
def create_person(name, phone_number):
    return {
        "name": name,
        "phone_number": phone_number
    }


# POST API to add a person
@app.post("/person")
def add_person(name: str, phone_number: str):
    global person_data

    # Call the function and store the details
    person_data = create_person(name, phone_number)

    # Return the stored details
    return person_data


# GET API to read person details
@app.get("/person")
def get_person():
    # Check whether person details are available
    if not person_data:
        return {"message": "No person details found"}

    # Copy the stored details
    result = person_data.copy()

    # Generate a random number between 1 and 100
    result["random_number"] = random.randint(1, 100)

    # Return the details with the random number
    return result
