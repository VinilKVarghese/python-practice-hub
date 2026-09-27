def get_variable_content_and_data_type(x):
    # Check for Boolean values
    if x.lower() == "true":
        x = True

    elif x.lower() == "false":
        x = False

    else:
        # Try to convert the value to an integer
        try:
            x = int(x)

        except ValueError:

            # If it is not an integer, try to convert it to a float
            try:
                x = float(x)

            except ValueError:
                # Keep it as a string
                pass

    # Return both the value and its data type
    return x, type(x).__name__


# Ask the user to enter a value
user_input = input("Enter any value: ")

# Call the function and store the returned values
data, data_type = get_variable_content_and_data_type(user_input)

# Print the data and its type
print("Variable Content-->" + str(data)+" Data Type-->" + str(data_type))

