from maze import *
from tkinter import messagebox

def main():
    win = Window(400,400)
    maze = Maze(0, 0, 12, 10, 25, 25, win)
    maze._draw_cell()
    maze._break_walls_r(0, 0)
    maze._reset_cells_visited()
    if maze._solve_r():
        messagebox.showinfo("", "Maze solved!")
    maze.win.wait_for_close()

main()
