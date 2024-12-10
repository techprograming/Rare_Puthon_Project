import random

# Initialize the Tic-Tac-Toe board
board = [' ' for _ in range(9)]

# Winning combinations
winning_combinations = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
    [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
    [0, 4, 8], [2, 4, 6]              # Diagonals
]

# Display the board
def print_board():
    print(f"{board[0]} | {board[1]} | {board[2]}")
    print("---------")
    print(f"{board[3]} | {board[4]} | {board[5]}")
    print("---------")
    print(f"{board[6]} | {board[7]} | {board[8]}")
    print()

# Check for a winner
def check_winner(player):
    for combination in winning_combinations:
        if all(board[i] == player for i in combination):
            return True
    return False

# Check if the board is full
def is_board_full():
    return ' ' not in board

# Minimax algorithm to determine the best move for AI
def minimax(board, depth, is_maximizing):
    if check_winner('X'):  # AI wins
        return 1
    elif check_winner('O'):  # Player wins
        return -1
    elif is_board_full():  # Draw
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'  # AI's move
                score = minimax(board, depth + 1, False)
                board[i] = ' '  # Undo the move
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'  # Player's move
                score = minimax(board, depth + 1, True)
                board[i] = ' '  # Undo the move
                best_score = min(score, best_score)
        return best_score

# Find the best move for the AI
def best_move():
    best_score = -float('inf')
    move = -1
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'X'  # AI's move
            score = minimax(board, 0, False)
            board[i] = ' '  # Undo the move
            if score > best_score:
                best_score = score
                move = i
    return move

# Play the game
def play_game():
    print("Tic-Tac-Toe: You are 'O', AI is 'X'.")
    print_board()

    while True:
        # Player's move
        player_move = int(input("Enter your move (1-9): ")) - 1
        if board[player_move] != ' ':
            print("Invalid move. Try again.")
            continue
        board[player_move] = 'O'
        print_board()

        if check_winner('O'):
            print("You win!")
            break
        elif is_board_full():
            print("It's a draw!")
            break

        # AI's move
        print("AI is making its move...")
        ai_move = best_move()
        board[ai_move] = 'X'
        print_board()

        if check_winner('X'):
            print("AI wins!")
            break
        elif is_board_full():
            print("It's a draw!")
            break

if __name__ == "__main__":
    play_game()
