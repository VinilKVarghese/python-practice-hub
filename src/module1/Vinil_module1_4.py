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
from datetime import datetime
def get_today_date():
    # Get today's date and time
    now = datetime.now()

    # Return date and time in the required format
    return now.strftime("%S:%M:%H, %d/%m/%Y")

# Call the function to get today's date and time
print("Printing today's date and time:", get_today_date())
# Call the function to print the Fibonacci sequence
fibonacci()