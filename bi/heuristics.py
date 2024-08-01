# Counts the number of connected pieces for the given player on the board.
# Connected pieces are those that form a horizontal or vertical line of the same color.
def count_connected(game, player):
    board = game.board
    color = player.color
    connected = 0
    
    # Iterate over each cell on the board
    for row in range(4):
        for col in range(4):
            # Check if the current cell contains the player's piece
            if board.array[row][col] == color:
                # Check horizontal connections
                for i in range(1, 4):
                    if col + i < 4 and board.array[row][col + i] == color:
                        connected += 1
                    else:
                        break

                # Check vertical connections (already partially done in horizontal check)
                connected += 1  # Count the current piece

                # Check diagonal connections
                for i in range(1, 4):
                    # Check down-right diagonal
                    if row + i < 4 and col + i < 4 and board.array[row + i][col + i] == color:
                        connected += 1
                    else:
                        break
                    
                    # Check up-right diagonal
                    if row - i >= 0 and col + i < 4 and board.array[row - i][col + i] == color:
                        connected += 1
                    else:
                        break
    return connected


# Evaluates the number of potential winning moves for both the player and the opponent.
# Potential wins are calculated based on empty spaces next to connected pieces.
def potential_wins(game):
    board = game.board
    color = game.player1.color
    opponent_color = game.player2.color
    
    def count_potential_wins(color):
        count = 0
        # Iterate over each cell on the board
        for row in range(4):
            for col in range(4):
                if board.array[row][col] == color:
                    # Check potential horizontal wins
                    if col < 3 and (board.array[row][col + 1] is None or board.array[row][col + 1] == color):
                        count += 1

                    # Check potential vertical wins
                    if row < 3 and board.array[row + 1][col] is None:
                        count += 1

                    # Check potential diagonal wins
                    if row < 3 and col < 3 and board.array[row + 1][col + 1] is None:
                        count += 1
                    if row > 0 and col < 3 and board.array[row - 1][col + 1] is None:
                        count += 1
        return count
    
    # Calculate the number of potential winning moves for the player
    player_potential_wins = count_potential_wins(color)
    
    # Calculate the number of potential winning moves for the opponent
    opponent_potential_wins = count_potential_wins(opponent_color)
    
    # Return the difference in potential wins between the player and the opponent
    # A higher value indicates a better position for the player
    return player_potential_wins - opponent_potential_wins


# Counts the number of empty cells on the board.
# More empty cells indicate more opportunities for placing pieces.
def empty_cells(game):
    board = game.board
    empty = 0
    # Iterate over each cell on the board
    for row in range(4):
        for col in range(4):
            # Check if the cell is empty
            if board.array[row][col] is None:
                empty += 1
    return empty


# Evaluates control over the central positions of the board.
# Controlling the center positions can be advantageous for strategy.
def center_control(game, player):
    center_positions = [(1, 1), (1, 2), (2, 1), (2, 2)]
    control = 0
    # Check if the player's pieces are in the central positions
    for row, col in center_positions:
        if game.board.array[row][col] == player.color:
            control += 1
    return control


# Calculates the heuristic score for blocking the opponent's potential wins.
# Preventing the opponent from winning is crucial for a defensive strategy.
def block_opponent_wins(game):
    opponent_wins = potential_wins(game)
    return -opponent_wins  # Return a negative value to reflect blocking


# Counts the number of lines being formed by the player's pieces.
# Forming lines can be a step towards winning or creating strategic positions.
def forming_lines(game, player):
    board = game.board
    color = player.color
    lines = 0
    
    # Iterate over each cell on the board
    for row in range(4):
        for col in range(4):
            # Check if the current cell contains the player's piece
            if board.array[row][col] == color:
                
                # Check for horizontal line formation
                if col + 1 < 4 and board.array[row][col + 1] == color:
                    lines += 1
                
                # Check for vertical line formation
                if row + 1 < 4 and board.array[row + 1][col] == color:
                    lines += 1
                
                # Check for down-right diagonal line formation
                if row + 1 < 4 and col + 1 < 4 and board.array[row + 1][col + 1] == color:
                    lines += 1
                
                # Check for up-right diagonal line formation
                if row - 1 >= 0 and col + 1 < 4 and board.array[row - 1][col + 1] == color:
                    lines += 1

    return lines


# Evaluates the board state and returns a heuristic score based on various factors.
# Higher scores are better for the `bi_player`, and lower (negative) scores indicate better positions for the opponent.
def evaluate(game, bi_player):
    # Check for a win or loss and assign extreme scores
    if game.check_winner() == bi_player.name:
        return float('inf')
    elif game.check_winner() == game.player2.name:
        return -float('inf')

    # Assign weights to different evaluation factors
    weight_connected = 2
    weight_potential_wins = 3
    weight_empty_cells = 1
    weight_center_control = 2
    weight_block_opponent_wins = 4
    weight_forming_lines = 2
    
    # Calculate the score by combining different factors
    score = (weight_connected * count_connected(game, bi_player) +
             weight_potential_wins * potential_wins(game) +
             weight_empty_cells * empty_cells(game) +
             weight_center_control * center_control(game, bi_player) +
             weight_block_opponent_wins * block_opponent_wins(game) +
             weight_forming_lines * forming_lines(game, bi_player))
    
    return score
