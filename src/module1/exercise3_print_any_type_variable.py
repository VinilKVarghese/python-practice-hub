def printVariableContentAndDataType():
    # Ask the user to enter a value
    x = input("Enter any value: ")

    # Check for Boolean values
    if x.lower() == "true":
        x = True
    elif x.lower() == "false":
        x = False
    else:
        # Try to convert to a number
        try:
            x = int(x)
        except ValueError:
            try:
                x = float(x)
            except ValueError:
                pass  # Keep it as a string

    # Print the value
    print(str(x) + " " + type(x).__name__)

# Call the function
printVariableContentAndDataType()
