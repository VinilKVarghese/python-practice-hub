def print_board(board: list[str]) -> None:
    """Prints the current 3x3 game board."""
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---|---|---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---|---|---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("\n")


def check_winner(board: list[str], player: str) -> bool:
    """Checks all 8 winning combinations (rows, columns, diagonals)."""
    win_conditions = [
        # Horizontal rows
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        # Vertical columns
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        # Diagonals
        [0, 4, 8],
        [2, 4, 6],
    ]

    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
            return True
    return False


def play_game() -> None:
    """Main game loop for two players."""
    # Initialize board with numbers 1-9 for positional guidance
    board = [str(i) for i in range(1, 10)]
    current_player = "X"
    moves_count = 0

    print("=============================")
    print("   WELCOME TO TIC-TAC-TOE   ")
    print("=============================")
    print("Players take turns entering a number (1-9) to place their mark.")

    while True:
        print_board(board)

        # Get and validate player input
        try:
            choice = int(input(f"Player '{current_player}', choose a position (1-9): "))
        except ValueError:
            print("Invalid input! Please enter a integer number between 1 and 9.")
            continue

        # Check bounds
        if choice < 1 or choice > 9:
            print("Out of bounds! Choose a number between 1 and 9.")
            continue

        # Check if square is already taken
        index = choice - 1
        if board[index] in ["X", "O"]:
            print("That spot is already taken! Pick another square.")
            continue

        # Place move
        board[index] = current_player
        moves_count += 1

        # Check win condition
        if check_winner(board, current_player):
            print_board(board)
            print(f"🎉 Congratulations! Player '{current_player}' wins!\n")
            break

        # Check draw condition
        if moves_count == 9:
            print_board(board)
            print("🤝 It's a draw! No more moves left.\n")
            break

        # Switch players
        current_player = "O" if current_player == "X" else "X"


if __name__ == "__main__":
    play_game()