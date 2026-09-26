def calculate_shifted_string_cost(text: str, letter_price: float) -> dict:
    """
    Shifts each letter in the string by one position in the alphabet, 
    counts total words, and calculates the total cost based on letter count.
    """
    shifted_chars = []
    
    for char in text:
        if 'a' <= char <= 'z':
            # Shift lowercase letter, wrap 'z' to 'a'
            shifted_char = chr((ord(char) - ord('a') + 1) % 26 + ord('a'))
            shifted_chars.append(shifted_char)
        elif 'A' <= char <= 'Z':
            # Shift uppercase letter, wrap 'Z' to 'A'
            shifted_char = chr((ord(char) - ord('A') + 1) % 26 + ord('A'))
            shifted_chars.append(shifted_char)
        else:
            # Leave punctuation, numbers, spaces unchanged
            shifted_chars.append(char)
            
    shifted_string = "".join(shifted_chars)
    word_count = len(text.split())
    
    # Price is calculated per letter (excluding spaces/punctuation)
    letter_count = sum(1 for char in text if char.isalpha())
    total_price = round(letter_count * letter_price, 2)
    
    return {
        "shifted_string": shifted_string,
        "word_count": word_count,
        "price_of_string": total_price
    }


# Example Usage:
result = calculate_shifted_string_cost("Hello World!", 0.25)
print(result)