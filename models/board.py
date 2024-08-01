from models.barrier import Barrier

class Board:
    # Initialize board to be an empty 4x4 grid and set the accessibility matrix
    def __init__(self):
        self.array = [[None for _ in range(4)] for _ in range(4)]
        self.accessibility = [
            [False, True, True, True],
            [True, True, True, True],
            [True, True, True, True],
            [True, True, True, False]
        ]
        self.active = True

    # Method to get the value at a specific cell
    def get_value(self, row, col):
        return self.array[row][col]
    
    # Check if a cell is accessible
    def is_accessible(self, col, row):
        return self.accessibility[row][col]

    # Add piece to the board based on the index and value, if the cell is accessible
    def add_piece(self, col, row, value):
        if self.is_accessible(col, row) and self.array[row][col] is None:
            self.array[row][col] = value
            return True
        else:
            return False

    # Method to move the piece on the board, if the destination cell is accessible
    def move_piece(self, col, row, new_col, new_row):
        # Check if the move is within one square distance (up, down, left, right, or diagonal)
        if abs(new_col - col) <= 1 and abs(new_row - row) <= 1:
            # Check if the new position is accessible and empty
            if self.is_accessible(new_col, new_row) and self.array[new_row][new_col] is None:
                # Move the piece
                self.array[new_row][new_col] = self.array[row][col]
                self.array[row][col] = None
                return True
        return False
    
    # Method to place a barrier on the board
    def place_barrier(self, col, row):
        if self.is_accessible(col, row) and self.array[row][col] is None:
            barrier = Barrier(col, row)
            self.array[row][col] = barrier
            self.accessibility[row][col] = False
            return True
        else:
            return False

    # Method to update the board, removing expired barriers
    def update_board(self):
        for row in range(4):
            for col in range(4):
                piece = self.array[row][col]
                if isinstance(piece, Barrier):
                    if not piece.decrement_turn():
                        self.array[row][col] = None
                        self.accessibility[row][col] = True


    # Method to deactivate the board
    def deactivate_board(self):
        self.active = False

    # Method to activate the board
    def activate_board(self):
        self.active = True