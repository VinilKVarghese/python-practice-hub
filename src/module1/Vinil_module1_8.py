# Open the address file and read its contents
with open("address.txt", "r") as file:
    lines = file.readlines()

# Initialize a variable to store the address
address = ""

# Read each line in the file
for line in lines:

    # Check if the line contains an address
    if line.startswith("Address:"):
        # Extract the address
        address = line.replace("Address:", "").strip()

        # Count the words in the address
        word_count = len(address.split())

        # Display the word count
        print("Address:", address)
        print("Word count:", word_count)

        # Append the word count to the same file
        with open("address.txt", "a") as file:
            file.write("Word count: " + str(word_count) + "\n")