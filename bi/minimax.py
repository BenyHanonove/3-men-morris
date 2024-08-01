from math import inf
from bi.heuristics import evaluate
import random


# Minimax algorithm with alpha-beta pruning for decision making in the game.
#Parameters:
#game (Game): The current game state.
#depth (int): The depth of the search tree.
#alpha (float): The best value that the maximizing player can guarantee.
#beta (float): The best value that the minimizing player can guarantee.
#maximizing_player (bool): True if the current move is for the maximizing player, False otherwise.
#bi_player (Player): The player for whom we are calculating the best move.
# Returns: tuple: The best evaluation score and the corresponding move.
    
def minimax(game, depth, alpha, beta, maximizing_player, bi_player):
    # Base case: if depth is 0 or the game is in an end state, return the evaluation of the board
    if depth == 0 or game.board.active:
        return evaluate(game, bi_player), None

    # Maximizing player's turn
    if maximizing_player:
        max_eval = float('-inf')  # Initialize to negative infinity
        best_move = None  # Best move initialization
        # Iterate over all possible legal moves for the maximizing player
        for move in game.get_legal_moves(bi_player):
            if move[0] == 'place_piece':
                _, col, row = move
                # Try the move
                if game.place_piece(col, row):
                    # Recursively call minimax for the next depth level
                    eval = minimax(game, depth - 1, alpha, beta, False, bi_player)[0]
                    # Undo the move
                    game.board.remove_piece(col, row)
                    bi_player.add_piece()
            elif move[0] == 'place_barrier':
                _, col, row = move
                # Try the move
                if game.place_barrier(col, row):
                    # Recursively call minimax for the next depth level
                    eval = minimax(game, depth - 1, alpha, beta, False, bi_player)[0]
                    # Undo the move
                    game.board.remove_barrier(col, row)
                    bi_player.add_barrier()
            elif move[0] == 'move_piece':
                _, col, row, new_col, new_row = move
                # Try the move
                if game.move_piece(col, row, new_col, new_row):
                    # Recursively call minimax for the next depth level
                    eval = minimax(game, depth - 1, alpha, beta, False, bi_player)[0]
                    # Undo the move
                    game.board.move_piece(new_col, new_row, col, row)

            # Update the best move found so far if the current evaluation is better
            if eval > max_eval:
                max_eval = eval
                best_move = move
            # Update alpha to the maximum value found so far
            alpha = max(alpha, eval)
            # Alpha-beta pruning: if beta is less than or equal to alpha, stop the search
            if beta <= alpha:
                break
        return max_eval, best_move

    # Minimizing player's turn
    else:
        min_eval = float('inf')  # Initialize to positive infinity
        opponent = game.get_opponent(bi_player)  # Get the opponent player
        best_move = None  # Best move initialization
        # Iterate over all possible legal moves for the minimizing player (opponent)
        for move in game.get_legal_moves(opponent):
            if move[0] == 'place_piece':
                _, col, row = move
                # Try the move
                if game.place_piece(col, row):
                    # Recursively call minimax for the next depth level
                    eval = minimax(game, depth - 1, alpha, beta, True, bi_player)[0]
                    # Undo the move
                    game.board.remove_piece(col, row)
                    opponent.add_piece()
            elif move[0] == 'place_barrier':
                _, col, row = move
                # Try the move
                if game.place_barrier(col, row):
                    # Recursively call minimax for the next depth level
                    eval = minimax(game, depth - 1, alpha, beta, True, bi_player)[0]
                    # Undo the move
                    game.board.remove_barrier(col, row)
                    opponent.add_barrier()
            elif move[0] == 'move_piece':
                _, col, row, new_col, new_row = move
                # Try the move
                if game.move_piece(col, row, new_col, new_row):
                    # Recursively call minimax for the next depth level
                    eval = minimax(game, depth - 1, alpha, beta, True, bi_player)[0]
                    # Undo the move
                    game.board.move_piece(new_col, new_row, col, row)

            # Update the best move found so far if the current evaluation is better
            if eval < min_eval:
                min_eval = eval
                best_move = move
            # Update beta to the minimum value found so far
            beta = min(beta, eval)
            # Alpha-beta pruning: if beta is less than or equal to alpha, stop the search
            if beta <= alpha:
                break
        return min_eval, best_move



# Determines the best placement for a piece for the given player using a combination of immediate win checks
# and Minimax evaluation.
# Parameters:
#     game (Game): The current game state.
#     depth (int): The depth of the search tree for Minimax.
#     player (Player): The player for whom we are calculating the best move.
# Returns: tuple: The best move (row, col) for placing a piece.

def bi_best_piece_place(game, depth, player):    
    # Get all possible moves for placing a piece and shuffle them to add randomness
    possible_moves = game.get_possible_pieces_places()
    random.shuffle(possible_moves)

    best_move = None  # Initialize best move
    blocking_move = None  # Initialize blocking move

    # Iterate over all possible moves
    for move in possible_moves:
        row, col = move
        # Temporarily place the piece on the board
        game.board.add_piece(col, row, player.color)

        # Check if this move results in a win for the player
        if game.check_winner() == player.name:
            game.board.array[row][col] = None  # Undo the move
            return move  # Return the winning move

        # Check if this move results in a win for the opponent
        opponent = game.player2
        if game.check_winner() == opponent.name:
            blocking_move = move  # Remember the move that blocks the opponent

        # Undo the move
        game.board.array[row][col] = None

    # If a blocking move was found, prioritize it
    if blocking_move:
        best_move = blocking_move
    else:
        best_score = -inf  # Initialize the best score to negative infinity

        # Evaluate all possible moves using Minimax
        for move in possible_moves:
            row, col = move
            # Temporarily place the piece on the board
            game.board.add_piece(col, row, player.color)

            # Use Minimax to evaluate the move
            score, _ = minimax(game, depth - 1, -float('inf'), float('inf'), False, player)
            # Undo the move
            game.board.array[row][col] = None

            # Update the best move if the current move has a higher score
            if score > best_score:
                best_score = score
                best_move = move

    # Return the best move if found, otherwise return the first possible move
    return best_move if best_move else possible_moves[0]



# Determines the best move for a piece for the given player using Minimax evaluation.
# Parameters:
#     game (Game): The current game state.
#     depth (int): The depth of the search tree for Minimax.
#     player (Player): The player for whom we are calculating the best move.
# Returns: tuple: The best move ((old_col, old_row), (new_col, new_row)) for moving a piece.

def bi_best_piece_move(game, depth, player):
    possible_moves = game.get_possible_pieces_moves(player)
    random.shuffle(possible_moves)

    best_move = None
    best_score = -float('inf')

    move_scores = []  # To collect all move scores

    for move in possible_moves:
        (old_col, old_row), (new_col, new_row) = move
        # Make the move
        game.board.move_piece(old_col, old_row, new_col, new_row)
        
        # Call minimax for the opponent's perspective
        score, _ = minimax(game, depth - 1, -float('inf'), float('inf'), False, player)
        move_scores.append((move, score))  # Collecting move and its score
        
        # Undo the move
        game.board.move_piece(new_col, new_row, old_col, old_row)

        # Update the best move if the current move is better
        if score > best_score:
            best_score = score
            best_move = move

    return best_move




# Determines the best placement for a barrier to block a winning move for the opponent.
# Parameters:
#     game (Game): The current game state.
# Returns: tuple or None: The best move (row, col) for placing a barrier to block the opponent, or None if no blocking move is found.

def bi_best_barrier_placement(game):
    opponent = game.player1

    # Create a copy of the game to simulate barrier placements without affecting the actual game state
    game_copy = game.copy()

    # Initialize a variable to store the move that blocks an opponent's winning move
    winning_move = None

    # Iterate through all possible barrier placements
    for move in game.get_possible_barrier_placements():
        row, col = move
        # Temporarily place a barrier in the copied game state
        game_copy.board.add_piece(col, row, opponent.color)  # Use the copy to modify the board

        # Check if the barrier placement results in a win for the opponent
        winner = game_copy.check_winner()
        if winner == opponent.name:
            winning_move = move
            break

        # Reset the barrier placement in the copied game state
        game_copy.board.array[row][col] = None
        game_copy.board.accessibility[row][col] = True

    if winning_move:
        return winning_move

    # If no blocking move is found, return None or any other default value
    return None
