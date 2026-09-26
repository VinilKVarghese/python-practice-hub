# Function to display the game board
def display_board(board):
    print()
    print(" " + board[0] + " | " + board[1] + " | " + board[2])
    print("---+---+---")
    print(" " + board[3] + " | " + board[4] + " | " + board[5])
    print("---+---+---")
    print(" " + board[6] + " | " + board[7] + " | " + board[8])
    print()


# Function to check if a player has won
def check_winner(board, player):
    # All possible winning combinations
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]

    # Check each winning combination
    for combination in winning_combinations:
        if all(board[i] == player for i in combination):
            return True

    return False


# Function to play the game
def play_game():
    # Initialize the board with numbers 1 to 9
    board = [str(i) for i in range(1, 10)]

    # Set the first player
    player = "X"

    # Count the number of moves
    moves = 0

    # Display the initial board
    display_board(board)

    # Continue until the game ends
    while moves < 9:
        try:
            # Ask the current player to choose a position
            choice = int(input("Player " + player + ", enter a number (1-9): "))

            # Check if the choice is valid
            if choice < 1 or choice > 9:
                print("Invalid choice! Enter a number from 1 to 9.")
                continue

            # Check if the position is already occupied
            if board[choice - 1] in ["X", "O"]:
                print("That position is already taken. Try again.")
                continue

            # Place the player's symbol on the board
            board[choice - 1] = player

            # Increase the move count
            moves += 1

            # Display the updated board
            display_board(board)

            # Check if the current player has won
            if check_winner(board, player):
                print("Player", player, "wins!")
                return

            # Switch to the other player
            if player == "X":
                player = "O"
            else:
                player = "X"

        except ValueError:
            # Handle invalid input
            print("Invalid input! Please enter a number.")

    # If all positions are filled and no one wins
    print("It's a draw!")


# Start the game
play_game()