import tkinter as tk 
from tkinter import messagebox ,simpledialog
from models.player import Player
from models.game import Game
from models.barrier import Barrier
from bi.minimax import bi_best_piece_place ,bi_best_piece_move ,bi_best_barrier_placement

class GameInterface:

    def __init__(self, root, game):
        # Initialize the depth for AI decision-making
        self.depth = 5

        # Store the root Tkinter window and the current game instance
        self.root = root
        self.game = game

        # Create and pack the frame for the game board
        self.board_frame = tk.Frame(root)
        self.board_frame.pack()

        # Create and display informational labels (e.g., player names, scores)
        self.create_info_labels()

        # Initialize a 4x4 grid of cells for the game board
        self.cells = [[None for _ in range(4)] for _ in range(4)]

        # Create and place the "New Game" button
        self.create_new_game_button()

        # Create and place the button for barrier placement mode
        self.create_barrier_button()

        # Create the game board cells in the UI
        self.create_board()

        # Initialize barrier placement mode flag
        self.barrier_placement_mode = False

        # Check if the current player is the AI (player2) and make the first move if so
        if self.game.current_player.name == self.game.player2.name:
            self.bi_place_piece()


    def create_info_labels(self):
        # Initialize info_frame here
        self.info_frame = tk.Frame(self.root)
        self.info_frame.pack(side=tk.BOTTOM)

        # Create a frame for current player info
        current_player_frame = tk.Frame(self.root)
        current_player_frame.pack(side=tk.TOP, pady=10)

        # Label for displaying current player with larger and bold text
        self.current_player_display = tk.Label(current_player_frame, text=f"Current Player: {self.game.current_player.name}({self.game.current_player.color})", font=("Helvetica", 14, "bold"))
        self.current_player_display.pack()

        # Player labels
        self.player1_label = tk.Label(self.info_frame, text=f"{self.game.player1.name}: {self.game.player1.color}")
        self.player1_label.pack(side=tk.LEFT, padx=20)

        self.player2_label = tk.Label(self.info_frame, text=f"{self.game.player2.name}: {self.game.player2.color}")
        self.player2_label.pack(side=tk.LEFT, padx=20)

        # Create a frame for barrier counter label
        info_labels_frame = tk.Frame(self.info_frame)
        info_labels_frame.pack(side=tk.TOP, pady=10)

        # Label for displaying barrier counters
        self.barrier_counter_label = tk.Label(info_labels_frame, text=f"Barriers - {self.game.player1.name}: {self.game.player1.barriers}  {self.game.player2.name}: {self.game.player2.barriers}")
        self.barrier_counter_label.pack(side=tk.LEFT, padx=20)


    def update_game(self):
        # Update the labels displaying player information
        self.player1_label.config(text=f"{self.game.player1.name}: {self.game.player1.color}")
        self.player2_label.config(text=f"{self.game.player2.name}: {self.game.player2.color}")
        
        # Update the display showing the current player
        self.current_player_display.config(text=f"Current Player: {self.game.current_player.name}({self.game.current_player.color})")
        
        # Update the barrier counter label to reflect the number of barriers each player has
        self.barrier_counter_label.config(text=f"Barriers - {self.game.player1.name}: {self.game.player1.barriers}  {self.game.player2.name}: {self.game.player2.barriers}")

        # Iterate through each cell in the 4x4 board
        for row in range(4):
            for col in range(4):
                cell_value = self.game.board.get_value(row, col)
                
                # If the cell contains a Barrier object
                if isinstance(cell_value, Barrier):
                    if cell_value.has_turn():
                        # Decrement the barrier's remaining turns if it is still active
                        cell_value.decrement_turn()
                    else:
                        # Remove the barrier if its turns have expired
                        self.game.board.array[row][col] = None
                        self.game.board.accessibility[row][col] = True
                        # Update the UI to reflect the removal of the barrier
                        if self.cells[row][col] is not None:
                            self.cells[row][col].configure(bg='light gray')
                
                # If the cell contains a Player object
                elif isinstance(cell_value, Player):
                    # Update the cell color to reflect the player's color
                    if self.cells[row][col] is not None:
                        self.cells[row][col].configure(bg=cell_value.color)

        # Refresh the UI to apply the updates
        self.root.update()


    def create_board(self):
        # Iterate over each cell position on the 4x4 board
        for row in range(4):
            for col in range(4):
                # Check if the cell is accessible for piece placement or movement
                if self.game.board.is_accessible(col, row):
                    # Create a button widget for each accessible cell
                    cell = tk.Button(
                        self.board_frame,  # The parent widget/frame where the button will be placed
                        text='',  # Initial text for the button (empty)
                        width=10,  # Width of the button
                        height=5,  # Height of the button
                        command=lambda r=row, c=col: self.cell_clicked(r, c),  # Command to execute on button click, passing current row and column
                        bg='light gray'  # Background color of the button (standard color)
                    )
                    # Place the button in the grid layout of the board_frame
                    cell.grid(row=row, column=col)
                    # Store a reference to the button in the cells array
                    self.cells[row][col] = cell


    def create_barrier_button(self):
        # Create a button to enable the barrier placement mode
        self.place_barrier_button = tk.Button(self.info_frame, text="Place Barrier", command=self.barrier_button_clicked, state=tk.NORMAL)
        self.place_barrier_button.pack(side=tk.RIGHT, padx=20)


    def create_new_game_button(self):
        # Create a button to start a new game
        self.new_game_button = tk.Button(self.info_frame, text="New Game", command=self.new_game)
        self.new_game_button.pack(side=tk.RIGHT, padx=20)


    def barrier_button_clicked(self):
        # Check if the game is currently active
        if not self.game.board.active:
            # Inform the user that the game is over and barrier placement is not allowed
            messagebox.showinfo("Game Over!", "The game is over.")
            return

        # Get the current player
        player = self.game.current_player

        # Check if the current player has barriers available for placement
        if player.has_barriers():
            # Prompt the user to confirm if they want to place a barrier
            action = messagebox.askquestion("Place Barrier", "Do you want to place a barrier?", icon='question', type=messagebox.YESNO)
            
            # If the user confirms they want to place a barrier
            if action == 'yes':
                # Set the barrier placement mode to True, allowing the player to select a cell for barrier placement
                self.barrier_placement_mode = True
                # Inform the user that they can now click on a cell to place a barrier
                messagebox.showinfo("Place Barrier", "Click on a cell to place a barrier.")
        else:
            # Inform the user that they have no barriers left to place
            messagebox.showinfo("Out of Barriers", "You are out of barriers.")


    def bi_place_piece(self):
        # First, handle the barrier placement for the AI before placing a new piece
        self.bi_barrier_place()

        # Check if the AI (player2) still has pieces to place
        if self.game.player2.has_pieces():
            # Determine the best placement for a new piece using the AI's strategy
            move = bi_best_piece_place(self.game, self.depth, self.game.player2)
            
            # If a valid move is found
            if move:
                row, col = move
                # Simulate a click on the selected cell to place the piece
                self.cell_clicked(row, col)


    def bi_piece_move(self):
        # First, attempt to place barriers using the AI's barrier placement strategy
        self.bi_barrier_place()
        
        # Determine the best piece move for the AI
        move = bi_best_piece_move(self.game, self.depth, self.game.player2)
        
        # If a valid move is found
        if move:
            (start_col, start_row), (end_col, end_row) = move

            # Ensure the start and end positions are within the board boundaries
            if (0 <= start_row < 4 and 0 <= start_col < 4) and (0 <= end_row < 4 and 0 <= end_col < 4):
                # Check if the AI has a piece at the start position
                if self.game.board.get_value(start_row, start_col) == self.game.player2.color:
                    # Check if the end position is empty
                    if self.game.board.get_value(end_row, end_col) is None:
                        # Ensure the move is valid (one square in any direction)
                        if abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1:
                            # Simulate a click on the start position to select the piece
                            select = self.cell_clicked(start_row, start_col)
                            if select:
                                # Simulate a click on the end position to move the piece
                                self.cell_clicked(end_row, end_col)


    def bi_barrier_place(self):
        # Get the AI player (player 2)
        bi_player = self.game.player2
        
        # While the AI has barriers left to place
        while bi_player.has_barriers():
            # Determine the best position for the AI to place a barrier
            barrier_move = bi_best_barrier_placement(self.game)
            
            # If a valid barrier placement position is found
            if barrier_move:
                row, col = barrier_move
                # Place the barrier on the game board
                self.game.place_barrier(col, row)
                # Update the UI to show the barrier placement
                self.cells[row][col].configure(bg='gray')
                # Update the barrier counter label to reflect the new state
                self.barrier_counter_label.config(text=f"Barriers - {self.game.player1.name}: {self.game.player1.barriers}  {self.game.player2.name}: {self.game.player2.barriers}")
            else:
                # No valid barrier placement found, exit the loop
                break


    def cell_clicked(self, row, col):
        # Get the current player from the game
        player = self.game.current_player

        # Check if the game is over
        if not self.game.board.active:
            messagebox.showinfo("Game Over!", "The game is over.")
            return False

        # Check if barrier placement mode is active
        if self.barrier_placement_mode:
            # Try to place a barrier at the clicked position
            if self.game.place_barrier(col, row):
                # Update the UI to reflect the barrier placement
                self.cells[row][col].configure(bg='gray')
                # Update the barrier count labels
                self.barrier_counter_label.config(text=f"Barriers - {self.game.player1.name}: {self.game.player1.barriers}  {self.game.player2.name}: {self.game.player2.barriers}")
                # Turn off barrier placement mode after placing a barrier
                self.barrier_placement_mode = False
                return True
            else:
                # Inform the user if the barrier placement is invalid
                messagebox.showinfo("Invalid Move", "You can't place a barrier there.")
                return False

        # Check if the current player has pieces left to place
        if self.game.current_player.has_pieces():
            # Try to place a new piece at the clicked position
            if self.game.place_piece(col, row):
                # Update the UI to reflect the piece placement
                self.cells[row][col].configure(bg=player.color)
                # Update the board state
                self.update_game()
                # Check if the move results in a win
                self.check_winner()
                # If the current player is not Morris BI, let AI make a move if it's player 2's turn
                if player.name != "Morris BI":
                    if self.game.player2.has_pieces():
                        self.bi_place_piece()
                    else:
                        self.bi_piece_move()
                return True
            else:
                # Inform the user if the piece placement is invalid
                messagebox.showinfo("Invalid Move", "You can't place a piece there.")
                return False
        else:
            # Check if there is a selected piece to move
            if self.game.selected_piece:
                start_row, start_col = self.game.selected_piece
                # Try to move the selected piece to the new position
                if self.move_piece(start_col, start_row, col, row):
                    # Update the UI to reflect the piece movement
                    self.cells[start_row][start_col].configure(bg='light gray')  # Clear old position
                    self.cells[row][col].configure(bg=player.color)  # Set new position
                    # Clear the selected piece
                    self.game.selected_piece = None
                    # Update the board state and check for a win
                    self.check_winner()
                    self.update_game()
                    # If the current player is not Morris BI, let AI make a move if it's player 2's turn
                    if player.name != "Morris BI":
                        if self.game.player2.has_pieces():
                            self.bi_place_piece()
                        else:
                            self.bi_piece_move()
                    return True
                else:
                    # Inform the user if the piece movement is invalid
                    messagebox.showinfo("Invalid Move", "You can't move the piece there.")
                    return False
            else:
                # No piece selected, check if the clicked cell contains the player's piece
                cell_value = self.game.board.get_value(row, col)
                if cell_value == player.color:
                    # Select the piece to move
                    self.game.selected_piece = (row, col)
                    # Inform the user that the piece has been selected
                    if player.name != "Morris BI":
                        messagebox.showinfo("Piece Selected", f"Selected piece at ({row}, {col}).")
                    return True
                else:
                    # Inform the user if the selection is invalid
                    messagebox.showinfo("Invalid Selection", "Select one of your pieces to move.")
                    return False


    def move_piece(self, start_col, start_row, new_col, new_row):
        # Attempt to move a piece on the game board
        if self.game.board.move_piece(start_col, start_row, new_col, new_row):
            # If the move is successful, switch to the next player
            self.game.switch_player()
            return True
        else:
            # If the move fails (invalid move or other issue), return False
            return False


    def new_game(self):
        # Create a new Player 1 with the same name as the current player1
        player1 = Player(name=self.game.player1.name)  # Default name for Player 1
        
        # Ensure Player 2 has a different color from Player 1
        while True:
            player2 = Player(name="Morris BI")
            if player1.color != player2.color:
                break

        # Initialize a new game with the new players
        game = Game(player1, player2)
        game.start()
        self.game.board.activate_board()  # Activate the game board for the new game

        # Update the GameInterface with the new game instance
        self.game = game

        # Reset the colors of all cells in the game interface to 'light gray'
        for row in range(4):
            for col in range(4):
                if self.cells[row][col] is not None:  # Check if cell widget exists
                    self.cells[row][col].configure(bg='light gray')

        # Update the game state in the interface
        self.update_game()
        
        # If the current player is Morris BI (AI), make the AI place a piece at the start of the game
        if self.game.current_player.name == self.game.player2.name:
            self.bi_place_piece()


    def check_winner(self):
        # Call the game's check_winner method to determine if there is a winner
        winner = self.game.check_winner()
        
        # If a winner is found, show an informational message box with the winner's name
        if winner:
            messagebox.showinfo("Game Over", f"{winner} wins!")
            
            # Deactivate the game board to prevent further moves
            self.game.board.deactivate_board()


if __name__ == "__main__":
    # Initialize the Tkinter root window
    root = tk.Tk()
    root.title("Three Men's Morris")  # Set the title of the window

    # Prompt the user to enter the name for Player 1
    player1_name = simpledialog.askstring("Input", "Enter name for Player 1:", parent=root)
    
    # If no name is provided, set a default name
    if not player1_name:
        player1_name = "Player 1"  # Default name if the user doesn't enter anything

    # Create an instance of Player 1 with the provided or default name
    player1 = Player(name=player1_name)

    # Ensure Player 2 has a different color from Player 1
    while True:
        player2 = Player(name="Morris BI")  # Create an instance of Player 2 with a fixed name
        if player1.color != player2.color:
            break  # Exit the loop if Player 2 has a different color

    # Initialize the Game object with the two players
    game = Game(player1, player2)
    game.start()  # Start the game

    # Create the GameInterface and pass the game instance to it
    app = GameInterface(root, game)

    # Start the Tkinter event loop
    root.mainloop()