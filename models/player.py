import random

class Player:
    # Initialize player with a name, color, 3 pieces and 2 barriers
    def __init__(self, name="BI"):
        self.name = name
        self.color = random.choice(self.available_colors)
        self.pieces = 3
        self.barriers = 2

    # Method to remove piece from user stack
    def remove_piece(self):
        if self.pieces > 0:
            self.pieces -= 1
            return True
        else:
            return False

    # Method to check if the player still has pieces 
    def has_pieces(self):
        return self.pieces > 0
    

    # Method to remove piece from user stack
    def remove_barrier(self):
        if self.barriers > 0:
            self.barriers -= 1
            return True
        else:
            return False

    # Method to check if the player still has pieces 
    def has_barriers(self):
        return self.barriers > 0

    # Predefined list of colors
    available_colors = ['orange', 'red', 'blue', 'green', 'yellow', 'purple']
