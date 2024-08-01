class Barrier:
    # Initialize barrier object
    def __init__(self ,vertical ,horizontal):
        self.turns_left = 4
        self.vertical = vertical
        self.horizontal = horizontal

    # Method to decrement the turns_left by one
    def decrement_turn(self):
        if self.turns_left > 0:
            self.turns_left -= 1
            return True
        else:
            return False
        
    # Method to decrement the turns_left by one
    def has_turn(self):
        if self.turns_left > 0:
            return True
        else:
            return False