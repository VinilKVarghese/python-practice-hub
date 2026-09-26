# Function to encrypt a string
def encrypt_string(text):
    try:
        # Check if the input is a string
        if not isinstance(text, str):
            raise TypeError("Input must be a string")

        # Initialize an empty string
        encrypted = ""

        # Go through each character
        for char in text:

            # Encrypt lowercase letters by shifting them backwards by 5 positions
            if char.islower() and char.isalpha():
                encrypted += chr((ord(char) - ord('a') - 5) % 26 + ord('a'))

            # Encrypt uppercase letters by shifting them backwards by 5 positions
            elif char.isupper() and char.isalpha():
                encrypted += chr((ord(char) - ord('A') -
                 5) % 26 + ord('A'))

            else:
                # Keep spaces, numbers, and symbols unchanged
                encrypted += char

        # Return the encrypted string
        return encrypted

    except TypeError as e:
        # Handle invalid input type
        print("Error:", e)
        return None

    except Exception as e:
        # Handle other unexpected errors
        print("Unexpected error:", e)
        return None


# Ask the user to enter a string
try:
    text = input("Enter a string to encrypt: ")

    # Display the encrypted string
    result = encrypt_string(text)

    if result is not None:
        print("Encrypted string:", result)

except Exception as e:
    print("Error:", e)