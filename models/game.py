import random
from models.board import Board
from models.barrier import Barrier
from copy import deepcopy

class Game:
    # Initialize Game with 2 new players
    def __init__(self, player1, player2):
        self.board = Board()
        self.player1 = player1
        self.player2 = player2
        self.current_player = None
        self.selected_piece = None
        self.active_barriers = [] 

    # Method to start the game
    def start(self):
        players = [self.player1, self.player2]
        self.current_player = random.choice(players)


    # Method to switch between players
    def switch_player(self):
        self.current_player = self.player1 if self.current_player == self.player2 else self.player2
        return self.current_player


    # Method to create a deep copy of the game state
    def copy(self):
        new_game = Game(deepcopy(self.player1), deepcopy(self.player2))
        new_game.board = deepcopy(self.board)
        new_game.current_player = deepcopy(self.current_player)
        new_game.selected_piece = deepcopy(self.selected_piece)
        new_game.active_barriers = deepcopy(self.active_barriers)
        return new_game


    # Method to place a new piece on the board
    def place_piece(self, col, row):
        if self.current_player.has_pieces() and self.board.add_piece(col, row, self.current_player.color):
            self.current_player.remove_piece()
            self.switch_player()
            return True
        return False
    

    # Method to place a barrier on the board
    def place_barrier(self, col, row):
        if self.current_player.has_barriers() and self.board.is_accessible(col, row):
            if self.board.place_barrier(col, row):
                barrier = Barrier(vertical=col, horizontal=row)  # Assuming col and row represent barrier position
                self.active_barriers.append(barrier)
                self.current_player.remove_barrier()
                return True
        return False


    # Method to move a piece on the board
    def move_piece(self, col, row, new_col, new_row):
        # Print the attempt details
        print(f"Attempting to move piece from ({col}, {row}) to ({new_col}, {new_row})")

        # Check if the current player has pieces and if the move is valid
        if self.current_player.has_pieces():
            print("Current player has pieces.")
            if self.board.move_piece(col, row, new_col, new_row):
                print("Piece successfully moved.")
                # Switch player after a successful move
                self.switch_player()
                print(f"Player switched. Current player: {self.current_player}")
                # Print the updated board state
                print("Updated board state:")
                self.print_board()
                return True
            else:
                print("Failed to move piece.")
        else:
            print("Current player has no pieces.")

        return False


    # Method to unselect the currently selected piece
    def unselect_piece(self):
        self.selected_piece = None


    # Method to select a piece to move
    def select_piece(self, col, row):
        if self.selected_piece == (col, row):
            self.unselect_piece()
            return False
        elif self.board.is_accessible(col, row) and self.board.array[row][col] == self.current_player.color:
            self.selected_piece = (col, row)
            return True
        return False


    # Method to check if there is a winner in the game
    def check_winner(self):
        winning_color = None

        # Check rows for a win
        for row in range(4):
            for col in range(2):
                # Check for three consecutive cells in the row with the same color
                if (self.board.array[row][col] == self.board.array[row][col+1] == self.board.array[row][col+2] 
                    and self.board.array[row][col] is not None):
                    winning_color = self.board.array[row][col]
                    break
            if winning_color:  # Exit outer loop if a winner is found
                break

        # Check columns for a win
        if winning_color is None:
            for col in range(4):
                for row in range(2):
                    # Check for three consecutive cells in the column with the same color
                    if (self.board.array[row][col] == self.board.array[row+1][col] == self.board.array[row+2][col] 
                        and self.board.array[row][col] is not None):
                        winning_color = self.board.array[row][col]
                        break
                if winning_color:  # Exit outer loop if a winner is found
                    break

        # Check diagonals for a win
        if winning_color is None:
            for row in range(2):
                for col in range(2):
                    # Check for three consecutive cells in the main diagonal (top-left to bottom-right)
                    if (self.board.array[row][col] == self.board.array[row+1][col+1] == self.board.array[row+2][col+2] 
                        and self.board.array[row][col] is not None):
                        winning_color = self.board.array[row][col]
                        break
                if winning_color:  # Exit outer loop if a winner is found
                    break

            if winning_color is None:
                for row in range(2):
                    for col in range(2, 4):
                        # Check for three consecutive cells in the anti-diagonal (top-right to bottom-left)
                        if (self.board.array[row][col] == self.board.array[row+1][col-1] == self.board.array[row+2][col-2] 
                            and self.board.array[row][col] is not None):
                            winning_color = self.board.array[row][col]
                            break
                    if winning_color:  # Exit outer loop if a winner is found
                        break

        # Determine the winner's name based on the winning color
        if winning_color:
            if self.player1.color == winning_color:
                winner_name = self.player1.name
            elif self.player2.color == winning_color:
                winner_name = self.player2.name
            return winner_name

        return None


    # Method to get the legal moves by player
    def get_legal_moves(self, player):
        legal_moves = []

        # Get all legal piece placement moves for the player
        if player.has_pieces():
            for row in range(4):
                for col in range(4):
                    # Check if the cell is accessible and empty
                    if self.board.is_accessible(col, row) and self.board.array[row][col] is None:
                        # Add move to place a piece to the list of legal moves
                        legal_moves.append(('place_piece', col, row))

        # Get all legal barrier placement moves for the player
        if player.has_barriers():
            for row in range(4):
                for col in range(4):
                    # Check if the cell is accessible and empty
                    if self.board.is_accessible(col, row) and self.board.array[row][col] is None:
                        # Add move to place a barrier to the list of legal moves
                        legal_moves.append(('place_barrier', col, row))

        # Get all legal piece movement moves for the player
        for start_row in range(4):
            for start_col in range(4):
                # Check if the current cell contains the player's piece
                if self.board.array[start_row][start_col] == player.color:
                    # Explore all possible directions for moving the piece
                    for d_row in [-1, 0, 1]:
                        for d_col in [-1, 0, 1]:
                            # Calculate the new position of the piece
                            if 0 <= start_row + d_row < 4 and 0 <= start_col + d_col < 4:
                                end_row = start_row + d_row
                                end_col = start_col + d_col
                                # Check if the new position is accessible and empty
                                if self.board.is_accessible(end_col, end_row) and self.board.array[end_row][end_col] is None:
                                    # Add move to move a piece to the list of legal moves
                                    legal_moves.append(('move_piece', start_col, start_row, end_col, end_row))

        return legal_moves


    # Method to get all possible places to place piece
    def get_possible_pieces_places(self):
        board = self.board
        possible_moves = []

        # Iterate over each cell in the 4x4 board
        for row in range(4):
            for col in range(4):
                # Check if the cell is accessible and currently empty
                if board.is_accessible(col, row) and board.array[row][col] is None:
                    # Add the cell as a possible move for placing a piece
                    possible_moves.append((row, col))

        return possible_moves


    # Method to get all possible places to move a piece
    def get_possible_pieces_moves(self, player):
        possible_piece_moves = []

        # Iterate over each cell in the 4x4 board
        for old_row in range(4):
            for old_col in range(4):
                # Check if the cell contains the player's piece
                if self.board.get_value(old_row, old_col) == player.color:
                    # Explore all possible directions for movement
                    for d_row in [-1, 0, 1]:
                        for d_col in [-1, 0, 1]:
                            # Skip the case where there's no movement
                            if d_row == 0 and d_col == 0:
                                continue

                            new_row = old_row + d_row
                            new_col = old_col + d_col

                            # Check if the new position is within the board boundaries
                            if 0 <= new_row < 4 and 0 <= new_col < 4:
                                # Check if the new position is accessible and empty
                                if self.board.is_accessible(new_col, new_row) and self.board.get_value(new_row, new_col) is None:
                                    # Add the move (from old position to new position) to the list
                                    possible_piece_moves.append(((old_col, old_row), (new_col, new_row)))

        return possible_piece_moves


    # Method to get all possible places to place barrier
    def get_possible_barrier_placements(self):
        board = self.board
        possible_moves = []

        # Iterate over each cell in the 4x4 board
        for row in range(4):
            for col in range(4):
                # Check if the cell is accessible and currently empty
                if board.is_accessible(col, row) and board.array[row][col] is None:
                    # Add the cell to possible barrier placements if it meets the criteria
                    possible_moves.append((row, col))

        return possible_moves
