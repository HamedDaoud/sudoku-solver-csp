import tkinter as tk
from solver import solve_sudoku
from sudoku_puzzles import PRE_GENERATED_SOLVED_GRIDS
import random

class SudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.difficulty = tk.StringVar(value='Hard')
        self.create_ui()
        self.initial_state = None
        self.final_state = None
        self.new_game()
        
    def create_ui(self):
        self.grid_frame = tk.Frame(self.root, bg='white')
        self.grid_frame.grid(row=0, column=0, columnspan=9, padx=10, pady=10)
        
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                border_width = {
                    "top": 3 if i % 3 == 0 else 1,
                    "left": 3 if j % 3 == 0 else 1,
                    "bottom": 3 if (i + 1) % 3 == 0 else 1,
                    "right": 3 if (j + 1) % 3 == 0 else 1
                }
                entry = tk.Entry(self.grid_frame, width=3, font=('Helvetica', 28), justify='center', fg='black', bg='#f0f0f0',
                                 relief="solid", bd=1)
                entry.grid(row=i, column=j, padx=(border_width["left"], 2), pady=(border_width["top"], 2), ipady=5)
                self.cells[i][j] = entry
        
        control_frame = tk.Frame(self.root, bg='white')
        control_frame.grid(row=10, column=0, columnspan=9, pady=(20, 10))
        
        self.new_game_button = tk.Button(control_frame, text="New Game", command=self.new_game, bg='#ffd700', fg='black', font=("Helvetica", 14, "bold"))
        self.new_game_button.pack(side=tk.LEFT, padx=10)
        
        self.solve_button = tk.Button(control_frame, text="Solve", command=self.solve_sudoku, bg='#00bfff', fg='white', font=("Helvetica", 14, "bold"))
        self.solve_button.pack(side=tk.LEFT, padx=10)
        
        difficulties = ["Easy", "Medium", "Hard"]
        for diff in difficulties:
            tk.Radiobutton(control_frame, text=diff, variable=self.difficulty, value=diff, bg='white', fg='black', selectcolor='#ffd700', font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)
        
    def new_game(self):
        for i in range(9):
            for j in range(9):
                entry = self.cells[i][j]
                entry.delete(0, tk.END)
                entry.config(state=tk.NORMAL, bg='#f0f0f0')
        
        self.final_state = random.choice(PRE_GENERATED_SOLVED_GRIDS)
        self.initial_state = [row[:] for row in self.final_state]
        
        num_remove = {'Easy': 30, 'Medium': 45, 'Hard': 60}[self.difficulty.get()]
        removed_positions = random.sample([(i, j) for i in range(9) for j in range(9)], num_remove)
        for i, j in removed_positions:
            self.initial_state[i][j] = 0
        
        for i in range(9):
            for j in range(9):
                value = self.initial_state[i][j]
                entry = self.cells[i][j]
                if value == 0:
                    entry.config(state=tk.NORMAL, bg='#f0f0f0')
                else:
                    entry.delete(0, tk.END)
                    entry.insert(0, str(value))
                    entry.config(state=tk.DISABLED)
        
        for i in range(9):
            for j in range(9):
                if self.initial_state[i][j] == 0:
                    self.cells[i][j].delete(0, tk.END)
        
    def solve_sudoku(self):
        grid = [[int(self.cells[i][j].get()) if self.cells[i][j].get().isdigit() else 0 for j in range(9)] for i in range(9)]
        
        solution = solve_sudoku(grid)
        if solution:
            for i in range(9):
                for j in range(9):
                    if self.initial_state[i][j] == 0:
                        self.cells[i][j].delete(0, tk.END)
                        self.cells[i][j].insert(0, str(solution[i][j]))
                        self.cells[i][j].config(bg="#d3ffd3")
        else:
            print("No solution found")

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()