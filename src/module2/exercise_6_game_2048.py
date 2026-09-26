import random

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


# Function to add a new tile (2 or 4)
def add_tile(board):
    # Find all empty positions
    empty = [(r, c) for r in range(4)
             for c in range(4) if board[r][c] == 0]

    # Add a tile to a random empty position
    if empty:
        r, c = random.choice(empty)
        board[r][c] = random.choices([2, 4], weights=[9, 1])[0]

    return board


# Function to merge a row towards the left
def merge_row(row):
    # Remove zeros from the row
    numbers = [num for num in row if num != 0]

    # Merge equal adjacent numbers
    result = []
    i = 0

    while i < len(numbers):
        if i + 1 < len(numbers) and numbers[i] == numbers[i + 1]:
            result.append(numbers[i] * 2)
            i += 2
        else:
            result.append(numbers[i])
            i += 1

    # Add zeros to make the row length 4
    result += [0] * (4 - len(result))

    return result


# Function to move the board in a given direction
def move_board(board, direction):
    # Create a copy of the original board
    old_board = [row[:] for row in board]

    # Move left
    if direction == "a":
        board = [merge_row(row) for row in board]

    # Move right
    elif direction == "d":
        board = [merge_row(row[::-1])[::-1] for row in board]

    # Move up
    elif direction == "w":
        board = list(map(list, zip(*board)))
        board = [merge_row(row) for row in board]
        board = [list(row) for row in zip(*board)]

    # Move down
    elif direction == "s":
        board = list(map(list, zip(*board)))
        board = [merge_row(row[::-1])[::-1] for row in board]
        board = [list(row) for row in zip(*board)]

    # Return the updated board and whether it changed
    return board, board != old_board


# Function to check if the player has reached 2048
def check_win(board):
    return any(2048 in row for row in board)


# Function to check if any moves are possible
def check_game_over(board):
    # Check for empty cells
    for row in board:
        if 0 in row:
            return False

    # Check for adjacent equal tiles horizontally
    for r in range(4):
        for c in range(3):
            if board[r][c] == board[r][c + 1]:
                return False

    # Check for adjacent equal tiles vertically
    for r in range(3):
        for c in range(4):
            if board[r][c] == board[r + 1][c]:
                return False

    return True


# Function to play the game
def play_game():
    # Create the board and add two starting tiles
    board = create_board()
    add_tile(board)
    add_tile(board)

    # Display the starting board
    display_board(board)

    # Keep playing until the game ends
    while True:
        # Ask the player for a move
        move = input("Enter W/A/S/D to move or Q to quit: ").lower()

        # Quit the game
        if move == "q":
            print("Game ended!")
            break

        # Check for valid input
        if move not in ["w", "a", "s", "d"]:
            print("Invalid input! Please enter W, A, S, D, or Q.")
            continue

        # Move the board
        board, changed = move_board(board, move)

        # Add a new tile only if the board changed
        if changed:
            add_tile(board)

        # Display the updated board
        display_board(board)

        # Check if the player reached 2048
        if check_win(board):
            print("Congratulations! You reached 2048!")
            break

        # Check if no moves are left
        if check_game_over(board):
            print("Game over! No more moves available.")
            break


# Start the game
play_game()