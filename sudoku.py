import tkinter as tk
from tkinter import messagebox, simpledialog
import random

class Sudoku:
    def __init__(self, root, difficulty):
        self.root = root
        self.difficulty = difficulty
        self.root.title("Sudoku Game")
        self.root.geometry("600x700")
        self.root.configure(bg="#f0f0f0")

        # Set size based on difficulty
        if difficulty == "easy":
            self.size = 3
        elif difficulty == "medium":
            self.size = 6
        else:
            self.size = 9

        self.board = [[0]*self.size for _ in range(self.size)]
        self.buttons = [[None]*self.size for _ in range(self.size)]

        self.title_label = tk.Label(
            root, text=f"Sudoku {difficulty.capitalize()}", font=("Helvetica", 20, "bold"),
            bg="#f0f0f0", fg="#333"
        )
        self.title_label.grid(row=0, column=0, columnspan=self.size, pady=(20, 10))

        for i in range(self.size):
            for j in range(self.size):
                button = tk.Button(
                    root, text=" ", font=("Helvetica", 18), width=3, height=1,
                    bg="#ffffff", fg="#000000", relief="solid", bd=1,
                    command=lambda row=i, col=j: self.on_click(row, col)
                )
                button.grid(row=i+1, column=j, padx=1, pady=1, ipadx=10, ipady=10)
                self.buttons[i][j] = button

        button_frame = tk.Frame(root, bg="#f0f0f0")
        button_frame.grid(row=self.size + 2, column=0, columnspan=self.size, pady=(10, 20))

        reset_btn = tk.Button(button_frame, text="Reset", font=("Helvetica", 12),
                              bg="#ffcccc", command=self.reset, width=10)
        reset_btn.pack(side=tk.LEFT, padx=5)

        solve_btn = tk.Button(button_frame, text="Solve", font=("Helvetica", 12),
                              bg="#ccffcc", command=self.solve_sudoku, width=10)
        solve_btn.pack(side=tk.LEFT, padx=5)

        check_btn = tk.Button(button_frame, text="Check", font=("Helvetica", 12),
                              bg="#ccccff", command=self.check_solution, width=10)
        check_btn.pack(side=tk.LEFT, padx=5)

        new_game_btn = tk.Button(button_frame, text="New Game", font=("Helvetica", 12),
                              bg="#ffffcc", command=self.new_game, width=10)
        new_game_btn.pack(side=tk.LEFT, padx=5)

        self.generate_board()

    def generate_board(self):
        """Randomly generates a partial board."""
        self.board = [[0]*self.size for _ in range(self.size)]

        numbers = list(range(1, self.size+1))
        # Randomly fill some cells
        if self.difficulty == "easy":
            cells_to_fill = (self.size * self.size) // 3  # ~33% filled
        elif self.difficulty == "medium":
            cells_to_fill = (self.size * self.size) // 4  # ~25% filled
        else:
            cells_to_fill = (self.size * self.size) // 5  # ~20% filled

        for _ in range(cells_to_fill):
            row, col = random.randint(0, self.size-1), random.randint(0, self.size-1)
            num = random.choice(numbers)
            while not self.is_valid(row, col, num) or self.board[row][col] != 0:
                row, col = random.randint(0, self.size-1), random.randint(0, self.size-1)
                num = random.choice(numbers)
            self.board[row][col] = num

        self.initial_board = [row[:] for row in self.board]

        for i in range(self.size):
            for j in range(self.size):
                num = self.board[i][j]
                text = str(num) if num != 0 else " "
                self.buttons[i][j].config(text=text, state="normal", fg="#000000")
                if num != 0:
                    self.buttons[i][j].config(state="disabled", fg="#555555")

    def on_click(self, row, col):
        if self.initial_board[row][col] == 0:
            self.input_number(row, col)

    def input_number(self, row, col):
        current_text = self.buttons[row][col].cget("text").strip()
        prompt_message = f"Enter number (1-{self.size}) for row {row+1}, column {col+1}:"

        if current_text != "":
            if not messagebox.askyesno("Change Number", f"Do you want to change the number {current_text}?"):
                return

        num = simpledialog.askinteger("Input", prompt_message, minvalue=1, maxvalue=self.size)
        if num is not None:
            self.board[row][col] = num
            self.buttons[row][col].config(text=str(num), fg="#0000ff")

    def solve_sudoku(self):
        if messagebox.askyesno("Confirm", "Solve this puzzle automatically?"):
            current_board = [row[:] for row in self.board]
            self.board = [row[:] for row in self.initial_board]

            if self.solve():
                for i in range(self.size):
                    for j in range(self.size):
                        self.buttons[i][j].config(
                            text=str(self.board[i][j]),
                            state="disabled" if self.initial_board[i][j] != 0 else "normal",
                            fg="#0000ff" if self.initial_board[i][j] == 0 else "#555555"
                        )
                messagebox.showinfo("Solved", "Puzzle solved!")
            else:
                self.board = current_board
                messagebox.showerror("Error", "No solution found!")

    def solve(self):
        empty = self.find_empty()
        if not empty:
            return True

        row, col = empty
        for num in range(1, self.size+1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.solve():
                    return True
                self.board[row][col] = 0
        return False

    def find_empty(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    return (i, j)
        return None

    def is_valid(self, row, col, num):
        for j in range(self.size):
            if self.board[row][j] == num:
                return False
        for i in range(self.size):
            if self.board[i][col] == num:
                return False
        box_size = int(self.size ** 0.5)
        box_row = (row // box_size) * box_size
        box_col = (col // box_size) * box_size
        for i in range(box_row, box_row + box_size):
            for j in range(box_col, box_col + box_size):
                if self.board[i][j] == num:
                    return False
        return True

    def check_solution(self):
        for row in self.board:
            if 0 in row:
                messagebox.showwarning("Incomplete", "Puzzle not complete yet!")
                return

        if self.validate_solution():
            messagebox.showinfo("Correct", "Congratulations! Your solution is correct!")
        else:
            messagebox.showerror("Incorrect", "There are mistakes. Keep trying!")

    def validate_solution(self):
        for row in self.board:
            if len(set(row)) != self.size or any(n < 1 or n > self.size for n in row):
                return False
        for col in range(self.size):
            column = [self.board[row][col] for row in range(self.size)]
            if len(set(column)) != self.size or any(n < 1 or n > self.size for n in column):
                return False
        box_size = int(self.size ** 0.5)
        for box_row_start in range(0, self.size, box_size):
            for box_col_start in range(0, self.size, box_size):
                box = []
                for i in range(box_row_start, box_row_start + box_size):
                    for j in range(box_col_start, box_col_start + box_size):
                        box.append(self.board[i][j])
                if len(set(box)) != self.size or any(n < 1 or n > self.size for n in box):
                    return False
        return True

    def reset(self):
        if messagebox.askyesno("Confirm", "Reset puzzle with new random numbers?"):
            self.generate_board()
    
    def new_game(self):
        if messagebox.askyesno("New Game", "Start a new game with different difficulty?"):
            self.root.destroy()
            start_game()

class DifficultySelector:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Difficulty")
        self.root.geometry("400x300")
        self.root.configure(bg="#f0f0f0")
        
        title_label = tk.Label(
            root, text="Choose Sudoku Difficulty", font=("Helvetica", 20, "bold"),
            bg="#f0f0f0", fg="#333", pady=30
        )
        title_label.pack()
        
        button_frame = tk.Frame(root, bg="#f0f0f0")
        button_frame.pack(pady=20)
        
        easy_btn = tk.Button(
            button_frame, text="Easy", font=("Helvetica", 16),
            bg="#ccffcc", width=10, command=lambda: self.start_game("easy")
        )
        easy_btn.pack(pady=10)
        
        medium_btn = tk.Button(
            button_frame, text="Medium", font=("Helvetica", 16),
            bg="#ccccff", width=10, command=lambda: self.start_game("medium")
        )
        medium_btn.pack(pady=10)
        
        hard_btn = tk.Button(
            button_frame, text="Hard", font=("Helvetica", 16),
            bg="#ffcccc", width=10, command=lambda: self.start_game("hard")
        )
        hard_btn.pack(pady=10)
    
    def start_game(self, difficulty):
        self.root.destroy()
        root = tk.Tk()
        Sudoku(root, difficulty)
        root.mainloop()

def start_game():
    root = tk.Tk()
    DifficultySelector(root)
    root.mainloop()

if __name__ == "__main__":
    start_game()
