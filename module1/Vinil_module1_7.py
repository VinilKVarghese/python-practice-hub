
# Function to accept and return a string
def display_string(value):
    try:
        # Check if the value is a string
        if not isinstance(value, str):
            raise TypeError("Not a string")

        # Return the string
        return value

    except TypeError:
        # Return None if the value is not a string
        return None


# Ask the user to enter a value
user_input = input("Enter any value: ")

# Try to convert the input into a number if possible
try:
    user_input = int(user_input)
except ValueError:
    try:
        user_input = float(user_input)
    except ValueError:
        pass  # Keep the value as a string

# Call the function and store the returned value
data = display_string(user_input)

# Print the returned value
print(data)

