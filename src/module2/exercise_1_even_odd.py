# Function to check if a number is even or odd
def check_even_odd(num):
    try:
        # Convert input to an integer
        num = int(num)

        # Check if the number is even or odd
        if num % 2 == 0:
            return "The number is Even"
        else:
            return "The number is Odd"

    except ValueError:
        # Return an error message for invalid input
        return "Invalid input! Please enter a valid integer."


# Ask the user to enter a number
number = input("Enter a number: ")

# Call the function and store the result
result = check_even_odd(number)

# Print the result
print(result)