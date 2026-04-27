import tkinter as tk
from tkinter import messagebox
import time
import copy

from puzzles import PUZZLES
from solver import get_solution


class SudokuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku AI Game")

        self.difficulty = "Easy"
        self.time_limit = 300

        self.start_game()

    def start_game(self):
        self.board = copy.deepcopy(PUZZLES[self.difficulty])
        self.solution = get_solution(self.board)

        if not isinstance(self.solution, list):
            raise Exception("Solution error")

        self.cells = []
        self.mistakes = 0
        self.start_time = time.time()
        self.game_over = False

        self.build_ui()
        self.update_timer()

    def build_ui(self):
        for w in self.root.winfo_children():
            w.destroy()

        tk.Label(self.root, text="Sudoku AI Game", font=("Arial", 18)).pack()

        # Difficulty buttons
        level_frame = tk.Frame(self.root)
        level_frame.pack(pady=5)

        tk.Button(level_frame, text="Easy",
                  command=lambda: self.set_level("Easy")).pack(side=tk.LEFT, padx=5)
        tk.Button(level_frame, text="Medium",
                  command=lambda: self.set_level("Medium")).pack(side=tk.LEFT, padx=5)
        tk.Button(level_frame, text="Hard",
                  command=lambda: self.set_level("Hard")).pack(side=tk.LEFT, padx=5)

        self.timer_label = tk.Label(self.root)
        self.timer_label.pack()

        self.mistake_label = tk.Label(self.root, text="Mistakes: 0")
        self.mistake_label.pack()

        frame = tk.Frame(self.root)
        frame.pack()

        self.cells = []

        for r in range(9):
            row = []
            for c in range(9):
                e = tk.Entry(frame, width=2, font=("Arial", 18), justify="center")
                e.grid(row=r, column=c)

                if self.board[r][c] != 0:
                    e.insert(0, str(self.board[r][c]))
                    e.config(state="disabled")
                else:
                    e.bind("<KeyRelease>", lambda event, r=r, c=c: self.check_input(r, c))

                row.append(e)
            self.cells.append(row)

        btn = tk.Frame(self.root)
        btn.pack(pady=10)

        tk.Button(btn, text="Hint", command=self.hint).grid(row=0, column=0)
        tk.Button(btn, text="Solve", command=self.solve).grid(row=0, column=1)
        tk.Button(btn, text="Check", command=self.check).grid(row=0, column=2)
        tk.Button(btn, text="New", command=self.start_game).grid(row=0, column=3)

    def set_level(self, level):
        self.difficulty = level

        if level == "Easy":
            self.time_limit = 300
        elif level == "Medium":
            self.time_limit = 600
        else:
            self.time_limit = 900

        self.start_game()

    def update_timer(self):
        if self.game_over:
            return

        elapsed = int(time.time() - self.start_time)
        remaining = self.time_limit - elapsed

        if remaining <= 0:
            self.time_up()
            return

        m, s = remaining // 60, remaining % 60
        self.timer_label.config(text=f"Time Left: {m:02d}:{s:02d}")

        self.root.after(1000, self.update_timer)

    def time_up(self):
        self.game_over = True
        messagebox.showinfo("Time Up", "Showing solution")

        for r in range(9):
            for c in range(9):
                self.fill_cell(r, c, True)

    def fill_cell(self, r, c, lock=False):
        val = self.solution[r][c]

        self.cells[r][c].config(state="normal")
        self.cells[r][c].delete(0, tk.END)
        self.cells[r][c].insert(0, str(val))

        if lock:
            self.cells[r][c].config(state="disabled")

    def check_input(self, r, c):
        val = self.cells[r][c].get()

        if val == "":
            return

        if not val.isdigit() or int(val) not in range(1, 10):
            self.cells[r][c].delete(0, tk.END)
            return

        val = int(val)

        if val != self.solution[r][c]:
            self.mistakes += 1
            self.mistake_label.config(text=f"Mistakes: {self.mistakes}")
            self.cells[r][c].config(bg="red")
        else:
            self.cells[r][c].config(bg="green")

    def hint(self):
        for r in range(9):
            for c in range(9):
                if self.cells[r][c].get() == "":
                    self.fill_cell(r, c)
                    return

    def solve(self):
        for r in range(9):
            for c in range(9):
                self.fill_cell(r, c, True)

    def check(self):
        for r in range(9):
            for c in range(9):
                val = self.cells[r][c].get()

                if val == "" or int(val) != self.solution[r][c]:
                    messagebox.showerror("Wrong", "Incorrect solution")
                    return

        messagebox.showinfo("Win", "Correct!")


root = tk.Tk()
SudokuGame(root)
root.mainloop()