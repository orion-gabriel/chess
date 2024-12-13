import chess
import tkinter as tk
from tkinter import messagebox


class ChessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Game")
        self.board = chess.Board()

        # Create UI components
        self.create_widgets()
        self.update_board_display()

    def create_widgets(self):
        # Chessboard display
        self.board_display = tk.Text(self.root, width=33, height=17, state="disabled", font=("Courier", 16))
        self.board_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Input field and submit button
        self.move_label = tk.Label(self.root, text="Enter your move (e.g., e2e4):")
        self.move_label.grid(row=1, column=0, sticky="w", padx=10)

        self.move_entry = tk.Entry(self.root)
        self.move_entry.grid(row=1, column=1, sticky="e", padx=10)

        # Buttons for submitting move and viewing legal moves
        self.submit_button = tk.Button(self.root, text="Submit Move", command=self.process_move)
        self.submit_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.legal_moves_button = tk.Button(self.root, text="See Legal Moves", command=self.display_legal_moves)
        self.legal_moves_button.grid(row=2, column=0, columnspan=2, pady=5)

        # Message display for game status
        self.message_label = tk.Label(self.root, text="", fg="blue")
        self.message_label.grid(row=4, column=0, columnspan=2, pady=5)

        # Restart and Quit buttons
        self.restart_button = tk.Button(self.root, text="Restart", command=self.restart_game)
        self.restart_button.grid(row=5, column=0, pady=10)

        self.quit_button = tk.Button(self.root, text="Quit", command=self.root.quit)
        self.quit_button.grid(row=5, column=1, pady=10)

    def update_board_display(self):
        """Update the chessboard display."""
        board_text = str(self.board)
        self.board_display.config(state="normal")
        self.board_display.delete(1.0, tk.END)
        self.board_display.insert(tk.END, board_text)
        self.board_display.config(state="disabled")

    def display_legal_moves(self):
        """Display all legal moves."""
        legal_moves = [self.board.san(move) for move in self.board.legal_moves]
        self.message_label.config(text=f"Legal Moves: {', '.join(legal_moves)}", fg="blue")

    def process_move(self):
        """Process the player's move."""
        next_move = self.move_entry.get().strip()
        legal_moves = [self.board.san(move) for move in self.board.legal_moves]

        # Validate the move
        if next_move not in legal_moves:
            self.message_label.config(text="Invalid move! Try again.", fg="red")
            return

        try:
            self.board.push_san(next_move)
            self.update_board_display()
            self.move_entry.delete(0, tk.END)

            # Check game status
            if self.board.is_checkmate():
                self.message_label.config(text="Checkmate! Game over.", fg="green")
                messagebox.showinfo("Game Over", "Checkmate! Game over.")
                self.disable_game()
            elif self.board.is_stalemate():
                self.message_label.config(text="Stalemate! Game over.", fg="green")
                messagebox.showinfo("Game Over", "Stalemate! Game over.")
                self.disable_game()
            elif self.board.is_check():
                self.message_label.config(text="Check!", fg="blue")
            else:
                self.message_label.config(text="Move successful!", fg="green")
        except Exception as e:
            self.message_label.config(text=f"Error: {e}", fg="red")

    def disable_game(self):
        """Disable game input after game over."""
        self.submit_button.config(state="disabled")
        self.move_entry.config(state="disabled")
        self.legal_moves_button.config(state="disabled")

    def restart_game(self):
        """Restart the game."""
        self.board = chess.Board()
        self.update_board_display()
        self.message_label.config(text="")
        self.submit_button.config(state="normal")
        self.move_entry.config(state="normal")
        self.legal_moves_button.config(state="normal")


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ChessApp(root)
    root.mainloop()
