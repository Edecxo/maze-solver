from maze import *

def main():
    win = Window(400,400)
    maze = Maze(0, 0, 12, 10, 25, 25, win)
    maze._draw_cell()
    maze._break_walls_r(0, 0)
    maze.win.wait_for_close()

main()
