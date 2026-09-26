import json

# Create a class to store person details
class Person:

    # Initialize the person's details
    def __init__(self, name, number, location, job_title):
        self.name = name
        self.number = number
        self.location = location
        self.job_title = job_title

    # Convert person details into a dictionary
    def to_dict(self):
        return {
            "name": self.name,
            "number": self.number,
            "location": self.location,
            "job_title": self.job_title
        }


# Function to save people details in a JSON file
def save_people(people):
    try:
        # Convert person objects into dictionaries
        data = [person.to_dict() for person in people]

        # Open the JSON file and save the details
        with open("people.json", "w") as file:
            json.dump(data, file, indent=4)

        # Return a success message
        return "People details saved successfully!"

    except (TypeError, OSError) as e:
        # Return an error message
        return "Error: " + str(e)


# Create an empty list to store person objects
people = []

# Ask the user to enter details for 5 people
for i in range(5):
    print("\nEnter details for person", i + 1)

    name = input("Enter name: ")
    number = input("Enter number: ")
    location = input("Enter location: ")
    job_title = input("Enter job title: ")

    # Create a person object
    person = Person(name, number, location, job_title)

    # Add the object to the list
    people.append(person)

# Call the function and store the result
result = save_people(people)

# Print the result
print(result)