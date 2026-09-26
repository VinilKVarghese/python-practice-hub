from datetime import datetime

def fibonacci():
    # Get the current minute
    minute = datetime.now().minute

    # Calculate the number of Fibonacci terms
    no_of_terms = 2 * minute

    # Print the number of terms
    print("Printing Fibonacci sequence up to", no_of_terms, "terms:")

    # Initialize the first two numbers
    a, b = 0, 1

    # Display the Fibonacci sequence
    for i in range(no_of_terms):
        print(a, end=" ")
        a, b = b, a + b

# Call the function
fibonacci()