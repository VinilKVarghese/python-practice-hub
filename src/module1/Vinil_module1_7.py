# Function to accept and display a string
def display_string(value):
    try:
        # Check if the value is a string
        if not isinstance(value, str):
            raise TypeError("Not a string")

        # Display the string
        print(value)

        # Return the string
        return value

    except TypeError:
        # Return None if the value is not a string
        return None


# Example
print(display_string("Hello World"))
print(display_string(123))