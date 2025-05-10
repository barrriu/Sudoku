import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

class Sudoku:
    def __init__(self, root, difficulty):
        self.root = root
        self.difficulty = difficulty
        self.root.title("Sudoku Game")
        self.root.geometry("600x700")
        self.root.configure(bg="#f0f0f0")

        self.board = [[0]*9 for _ in range(9)]
        self.buttons = [[None]*9 for _ in range(9)]

        # Title
        self.title_label = tk.Label(
            root, text="Sudoku Game", font=("Helvetica", 20, "bold"),
            bg="#f0f0f0", fg="#333"
        )
        self.title_label.grid(row=0, column=0, columnspan=9, pady=(20, 10))

        # Sudoku board buttons
        for i in range(9):
            for j in range(9):
                button = tk.Button(
                    root, text=" ", font=("Helvetica", 18), width=3, height=1,
                    bg="#ffffff", fg="#000000", relief="solid", bd=1,
                    command=lambda row=i, col=j: self.on_click(row, col)
                )
                button.grid(row=i+1, column=j, padx=1, pady=1, ipadx=10, ipady=10)
                self.buttons[i][j] = button

        # Control buttons
        button_frame = tk.Frame(root, bg="#f0f0f0")
        button_frame.grid(row=10, column=0, columnspan=9, pady=(10, 20))

        reset_btn = tk.Button(
            button_frame, text="Reset", font=("Helvetica", 12),
            bg="#ffcccc", command=self.reset, width=10
        )
        reset_btn.pack(side=tk.LEFT, padx=5)

        solve_btn = tk.Button(
            button_frame, text="Solve", font=("Helvetica", 12),
            bg="#ccffcc", command=self.solve_sudoku, width=10
        )
        solve_btn.pack(side=tk.LEFT, padx=5)

        check_btn = tk.Button(
            button_frame, text="Check", font=("Helvetica", 12),
            bg="#ccccff", command=self.check_solution, width=10
        )
        check_btn.pack(side=tk.LEFT, padx=5)

        self.generate_board()
        # Note: The grid lines drawing is somewhat disconnected from the buttons' grid
        # placement in the original code's logic. The canvas is placed separately.
        # For a more integrated look, you might need to adjust grid placement
        # or draw lines directly on the button frames.
        # self.draw_grid_lines() # Leaving this commented out as it overlaps/misaligns with the button grid by default.

    def draw_grid_lines(self):
        # This method is present in your code but might cause visual
        # misalignment with the button grid due to separate grid placements.
        # It's kept here as per your original code but is commented out in __init__.
        canvas = tk.Canvas(self.root, width=450, height=450, bg="white", bd=0, highlightthickness=0)
        canvas.grid(row=1, column=0, rowspan=9, columnspan=9, padx=15, pady=(0, 10))

        # Draw thick lines for 3x3 boxes
        for i in range(1, 3):
            canvas.create_line(i * 150, 0, i * 150, 450, width=3, fill="black")
            canvas.create_line(0, i * 150, 450, i * 150, width=3, fill="black")

        # Draw thin lines for cells
        for i in range(1, 9):
            canvas.create_line(i * 50, 0, i * 50, 450, width=1, fill="gray")
            canvas.create_line(0, i * 50, 450, i * 50, width=1, fill="gray")


    def generate_board(self):
        # Initialize with the board from your image
        self.board = [
            [5, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        # Display the board
        for i in range(9):
            for j in range(9):
                num = self.board[i][j]
                text = str(num) if num != 0 else " "
                self.buttons[i][j].config(text=text, state="normal", fg="#000000") # Always enable for user input
                if num != 0:
                     self.buttons[i][j].config(state="disabled", fg="#555555") # Visually distinct and disabled for initial numbers


    def on_click(self, row, col):
        # Allow input/reinput on any cell that wasn't part of the initial puzzle
        # Check if the cell was initially empty (0) to prevent changing starting numbers
        initial_board_state = [ # Re-define the initial state to check against
            [5, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        if initial_board_state[row][col] == 0:
             self.input_number(row, col)
        # The reinput logic for *initial* numbers was likely unintended,
        # the original code allowed it. The check above prevents changing
        # starting numbers, which is more standard Sudoku behavior.
        # If you want to allow reinput on initial numbers, remove the if condition.


    def input_number(self, row, col):
        # Get current text to see if it's empty or already has a number
        current_text = self.buttons[row][col].cget("text").strip()
        prompt_message = f"Enter number (1-9) for row {row+1}, column {col+1}:"

        if current_text != "":
            # If already has a number, confirm if user wants to change
            if not messagebox.askyesno("Change Number", f"Do you want to change the number {current_text} at row {row+1}, column {col+1}?"):
                return # User cancelled

        num = simpledialog.askinteger("Input", prompt_message,
                                     minvalue=1, maxvalue=9)
        if num is not None: # simpledialog returns None if cancelled
            self.board[row][col] = num
            self.buttons[row][col].config(text=str(num), fg="#0000ff") # Change color for user input


    # The original reinput_number method is integrated into input_number now
    # def reinput_number(self, row, col):
    #     if messagebox.askyesno("Confirm", "Change existing number?"):
    #         self.input_number(row, col)


    def solve_sudoku(self):
        """Solves the Sudoku using backtracking algorithm"""
        if messagebox.askyesno("Confirm", "Solve this puzzle? This will fill in the correct numbers."):
            # Make a copy of the current board state to potentially restore
            current_board_state = [row[:] for row in self.board]

            # Clear the board of user inputs, keeping only initial numbers for solving
            initial_board_for_solving = [
                [5, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [6, 0, 0, 1, 9, 5, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]
            self.board = [row[:] for row in initial_board_for_solving] # Start solving from the initial state

            if self.solve():
                messagebox.showinfo("Solved", "Puzzle solved successfully!")
                # Update GUI with the solved board
                for i in range(9):
                    for j in range(9):
                         text = str(self.board[i][j])
                         self.buttons[i][j].config(text=text, state="disabled" if initial_board_for_solving[i][j] != 0 else "normal", fg="#000000") # Display solution, initial numbers disabled, solved numbers enabled
                         if initial_board_for_solving[i][j] == 0:
                             self.buttons[i][j].config(fg="#0000ff") # Solved numbers in different color
            else:
                messagebox.showerror("Error", "No solution exists for the initial puzzle!")
                # Restore the board state before trying to solve
                self.board = current_board_state
                self.generate_board() # Redraw the board based on the restored state


    def solve(self):
        """Backtracking solver implementation"""
        empty = self.find_empty()
        if not empty:
            return True # Base case: no empty cells means puzzle is solved

        row, col = empty

        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                # Optional: Update GUI during solving to visualize (can be slow for complex puzzles)
                # self.buttons[row][col].config(text=str(num), fg="#00cc00") # Green for solving attempt
                # self.root.update_idletasks() # Update display

                if self.solve(): # Recursively try to solve the rest of the puzzle
                    return True

                # If the recursive call returns False, backtrack
                self.board[row][col] = 0 # Reset the cell
                # Optional: Update GUI during backtracking
                # self.buttons[row][col].config(text=" ", fg="#000000")
                # self.root.update_idletasks()

        return False # No number worked in this cell, trigger backtracking in the previous step


    def find_empty(self):
        """Finds next empty cell (0) row by row, column by column"""
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return (i, j) # Return row, column tuple
        return None # No empty cell found


    def is_valid(self, row, col, num):
        """Checks if num can be placed at (row, col) according to Sudoku rules"""
        # Check row
        if num in self.board[row]:
            return False

        # Check column
        if num in [self.board[i][col] for i in range(9)]:
            return False

        # Check 3x3 box
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.board[i][j] == num:
                    return False

        return True # If all checks pass, the number is valid


    def check_solution(self):
        """Checks if the current board state is a valid and complete Sudoku solution"""
        # First, check if the board is full
        for row in self.board:
            if 0 in row:
                messagebox.showwarning("Incomplete", "Puzzle is not complete yet! Fill all the empty cells.")
                return

        # Then, validate the filled board
        if self.validate_solution():
            messagebox.showinfo("Correct", "Congratulations! Your solution is correct!")
        else:
            messagebox.showerror("Wrong", "Your solution contains errors. Keep trying!")


    def validate_solution(self):
        """Validates the current board state against Sudoku rules"""
        # Check rows
        for row in self.board:
            # Using set converts the list to a set, removing duplicates.
            # A valid row has 9 unique numbers from 1 to 9.
            # Also check if all numbers are within the valid range (1-9) and not 0.
            if len(set(row)) != 9 or any(n < 1 or n > 9 for n in row):
                return False

        # Check columns
        for col in range(9):
            column = [self.board[row][col] for row in range(9)]
            if len(set(column)) != 9 or any(n < 1 or n > 9 for n in column):
                return False

        # Check 3x3 boxes
        for box_row_start in range(0, 9, 3):
            for box_col_start in range(0, 9, 3):
                box = []
                for i in range(box_row_start, box_row_start + 3):
                    for j in range(box_col_start, box_col_start + 3):
                        box.append(self.board[i][j])
                if len(set(box)) != 9 or any(n < 1 or n > 9 for n in box):
                    return False

        return True # If all checks pass, the solution is valid


    def reset(self):
        """Resets the board to its initial state"""
        if messagebox.askyesno("Confirm", "Reset the puzzle to the original state?"):
            self.generate_board()


def start_game():
    """Initializes the Tkinter root window and starts the game"""
    root = tk.Tk()
    Sudoku(root, "medium")  # 'medium' is just a label here, the board is hardcoded
    root.mainloop()

if __name__ == "__main__":
    start_game()