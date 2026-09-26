# Create a class to store person details
class Person:

    # Initialize the person's details
    def __init__(self, name, contact, address, phone_number):
        self.name = name
        self.contact = contact
        self.address = address
        self.phone_number = phone_number

    # Save the person's details to a text file
    def save_to_file(self):
        with open("address.txt", "a") as file:
            file.write("Name: " + self.name + "\n")
            file.write("Contact: " + self.contact + "\n")
            file.write("Address: " + self.address + "\n")
            file.write("Phone Number: " + self.phone_number + "\n")
            file.write("----------------------\n")

        print("Address saved successfully!")


# Ask the user to enter the person's details
name = input("Enter name: ")
contact = input("Enter contact: ")
address = input("Enter address: ")
phone_number = input("Enter phone number: ")

# Create an object of the Person class
person1 = Person(name, contact, address, phone_number)

# Save the details to the text file
person1.save_to_file()