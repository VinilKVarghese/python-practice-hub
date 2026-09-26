# Function to find unique numbers in a list
def find_unique(numbers):
    try:
        # Remove duplicates from the list
        unique_numbers = list(set(numbers))

        # Return the unique numbers
        return unique_numbers

    except TypeError:
        # Return an error message for invalid input
        return "Invalid input! Please enter a list of numbers."


# Ask the user to enter numbers separated by spaces
user_input = input("Enter numbers separated by spaces: ")

try:
    # Convert the input into a list of integers
    numbers = list(map(int, user_input.split()))

    # Call the function and store the result
    result = find_unique(numbers)

    # Print the result
    print("Unique numbers:", result)

except ValueError:
    # Handle invalid number input
    print("Invalid input! Please enter valid numbers.")