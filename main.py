from drawers import *

def main():
    win = Window(800, 600) 
    '''
    cell1 = Cell(Point(20,20), Point(40, 40))
    cell2 = Cell(Point(50, 20), Point(70, 40))
    win.draw_cell(cell1, "black")
    win.draw_cell(cell2, "black")
    cell1.cell_move(win.canvas, cell2)
    win.wait_for_close()
    '''
    maze = Maze(0, 0, 10, 10, 20, 20, win)
    maze._draw_cell(200, 200)

main()
