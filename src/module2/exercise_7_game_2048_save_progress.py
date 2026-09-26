
import random
import json
import os

# File to store the game session
SAVE_FILE = "game_save.json"


# Function to create an empty 4x4 board
def create_board():
    return [[0] * 4 for _ in range(4)]


# Function to display the board
def display_board(board):
    print("\n+------+------+------+------+")

    for row in board:
        print("|", end="")
        for num in row:
            if num == 0:
                print("      |", end="")
            else:
                print(f"{num:^6}|", end="")
        print("\n+------+------+------+------+")


# Function to add a new tile
def add_tile(board):
    empty = [
        (r, c) for r in range(4)
        for c in range(4) if board[r][c] == 0
    ]

    if empty:
        r, c = random.choice(empty)
        board[r][c] = random.choices(
            [2, 4], weights=[9, 1]
        )[0]

    return board


# Function to merge a row towards the left
def merge_row(row):
    numbers = [num for num in row if num != 0]
    result = []
    i = 0

    while i < len(numbers):
        if i + 1 < len(numbers) and numbers[i] == numbers[i + 1]:
            result.append(numbers[i] * 2)
            i += 2
        else:
            result.append(numbers[i])
            i += 1

    result += [0] * (4 - len(result))
    return result


# Function to move the board
def move_board(board, direction):
    old_board = [row[:] for row in board]

    if direction == "a":
        board = [merge_row(row) for row in board]

    elif direction == "d":
        board = [merge_row(row[::-1])[::-1] for row in board]

    elif direction == "w":
        board = [list(row) for row in zip(*board)]
        board = [merge_row(row) for row in board]
        board = [list(row) for row in zip(*board)]

    elif direction == "s":
        board = [list(row) for row in zip(*board)]
        board = [merge_row(row[::-1])[::-1] for row in board]
        board = [list(row) for row in zip(*board)]

    return board, board != old_board


# Function to save the current game
def save_game(board):
    try:
        # Open the file and save the board as JSON
        with open(SAVE_FILE, "w") as file:
            json.dump(board, file, indent=4)

        return "Game saved successfully!"

    except (OSError, TypeError) as e:
        return "Error saving game: " + str(e)


# Function to load a saved game
def load_game():
    try:
        # Check whether a saved game exists
        if not os.path.exists(SAVE_FILE):
            return None

        # Read the saved board from the JSON file
        with open(SAVE_FILE, "r") as file:
            board = json.load(file)

        # Validate the board structure
        if (
            isinstance(board, list)
            and len(board) == 4
            and all(
                isinstance(row, list)
                and len(row) == 4
                and all(type(num) is int and num >= 0 for num in row)
                for row in board
            )
        ):
            return board

        return None

    except (OSError, json.JSONDecodeError):
        return None


# Function to check if the player has reached 2048
def check_win(board):
    return any(2048 in row for row in board)


# Function to check if the game is over
def check_game_over(board):
    for row in board:
        if 0 in row:
            return False

    for r in range(4):
        for c in range(3):
            if board[r][c] == board[r][c + 1]:
                return False

    for r in range(3):
        for c in range(4):
            if board[r][c] == board[r + 1][c]:
                return False

    return True


# Function to start or continue the game
def play_game():
    # Ask the user whether to continue or start a new game
    print("\n--- 2048 GAME ---")
    print("1. Continue saved game")
    print("2. Start new game")
    print("3. Quit")

    choice = input("Enter your choice: ")

    # Load the saved game or create a new board
    if choice == "1":
        board = load_game()

        if board is None:
            print("No valid saved game found. Starting a new game.")
            board = create_board()
            add_tile(board)
            add_tile(board)

    elif choice == "2":
        board = create_board()
        add_tile(board)
        add_tile(board)

    elif choice == "3":
        print("Goodbye!")
        return

    else:
        print("Invalid choice!")
        return

    # Display the board
    display_board(board)

    # Main game loop
    while True:
        move = input(
            "Enter W/A/S/D to move or Q to quit: "
        ).lower()

        # Quit while keeping the saved session
        if move == "q":
            print(save_game(board))
            print("You can continue later!")
            break

        # Validate the direction
        if move not in ["w", "a", "s", "d"]:
            print("Invalid input! Enter W, A, S, D, or Q.")
            continue

        # Move the board
        board, changed = move_board(board, move)

        # Add a new tile only if the board changed
        if changed:
            add_tile(board)

            # Save the updated board
            print(save_game(board))

        # Display the updated board
        display_board(board)

        # Check if the player has won
        if check_win(board):
            print("Congratulations! You reached 2048!")
            save_game(board)
            break

        # Check if the game is over
        if check_game_over(board):
            print("Game over! No more moves available.")
            save_game(board)
            break


# Start the game
play_game()