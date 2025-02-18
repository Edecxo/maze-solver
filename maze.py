from tkinter import Tk, BOTH, Canvas
import random
import time

class Window():
    def __init__(self, width, height, title=None):
        self.width = width
        self.height = height
        self.root_widget = Tk()
        self.root_widget.geometry(f"{self.width}x{self.height}")
        self.root_widget.title = title
        self.root_widget.protocol("WM_DELETE_WINDOW", self.close)
        self.canvas = Canvas(self.root_widget, width=self.width, height=self.height, bg="white")
        self.canvas.pack()
        self.is_running = False

    def redraw(self):
        self.canvas.update_idletasks()
        self.canvas.update()

    def wait_for_close(self):
        self.is_running = True
        while self.is_running:
            self.redraw()

    def close(self):
        self.is_running = False

    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)

    def draw_cell(self, cell, fill_color):
        cell.draw(self.canvas, fill_color)

class Point():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        
    def __add__(self, other):
        return Point(
                self.x + other.x,
                self.y + other.y
        )

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

class Line():
    def __init__(self, point_a, point_b):
        self.point_a = point_a
        self.point_b = point_b

    def draw(self, canvas, fill_color):
        canvas.create_line(
                self.point_a.x, self.point_a.y,
                self.point_b.x, self.point_b.y,
                fill=fill_color, width=2
        )

class Cell():
    def __init__(self, top_left, bottom_right):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self._x1 = top_left.x
        self._y1 = top_left.y
        self._x2 = bottom_right.x
        self._y2 = bottom_right.y
        self.has_left_wall  = True
        self.has_right_wall = True
        self.has_top_wall   = True
        self.has_bottom_wall= True
        self.visited = False

    def draw(self, canvas, fill_color="black"):
        bg_color = "white"
        left_wall = Line(self.top_left, Point(self.top_left.x, self.bottom_right.y))
        if self.has_left_wall:
            left_wall.draw(canvas, fill_color)
        else:
            left_wall.draw(canvas, bg_color)

        right_wall = Line(Point(self.bottom_right.x, self.top_left.y), self.bottom_right)
        if self.has_right_wall:
            right_wall.draw(canvas, fill_color)
        else:
            right_wall.draw(canvas, bg_color)
            
        top_wall = Line(self.top_left, Point(self.bottom_right.x, self.top_left.y))
        if self.has_top_wall:
            top_wall.draw(canvas, fill_color)
        else:
            top_wall.draw(canvas, bg_color)

        bottom_wall = Line(Point(self.top_left.x, self.bottom_right.y), self.bottom_right)
        if self.has_bottom_wall:
            bottom_wall.draw(canvas, fill_color)
        else:
            bottom_wall.draw(canvas, bg_color)

    def cell_move(self, canvas, to_cell, undo=False):
        from_cell_center = Point(
                min(self._x1, self._x2) + (max(self._x1, self._x2) - min(self._x1, self._x2)) / 2,
                min(self._y1, self._y2) + (max(self._y1, self._y2) - min(self._y1, self._y2)) / 2
        )
        min(to_cell._y1, to_cell._y2)
        to_cell_center = Point(
                min(to_cell._x1, to_cell._x2) + (max(to_cell._x1, to_cell._x2) - min(to_cell._x1, to_cell._x2)) / 2,
                min(to_cell._y1, to_cell._y2) + (max(to_cell._y1, to_cell._y2) - min(to_cell._y1, to_cell._y2)) / 2
        )
        fill_color = "red"
        if undo:
            fill_color = "grey"
        line = Line(from_cell_center, to_cell_center)
        line.draw(canvas, fill_color)

    def update(self):
        self._x1 = self.top_left.x
        self._y1 = self.top_left.y
        self._x2 = self.bottom_right.x
        self._y2 = self.bottom_right.y
     
    def __repr__(self):
        return f"Cell(({self._x1}, {self._y1}), ({self._x2}, {self._y2}))"

    def cell_walls(self):
        return f"L:{self.has_left_wall},R:{self.has_right_wall},T:{self.has_top_wall},B:{self.has_bottom_wall}"

class Maze():
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win,
        seed=None,
        offset=Point(2, 2)
    ):
        self._x1 = x1
        self._y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.offset = offset
        if seed:
            self.seed = random.seed(seed)
        self.maze_size = None #created with _draw_cell()
        self._cells = []
        self._create_cells()

    def _create_cells(self):
        for i in range(self.num_rows):
            self._cells.append([])
        cell_top_left = self.offset
        cell_bottom_right = self.offset
        for row in self._cells:
            for i in range(self.num_cols):
                row.append(Cell(cell_top_left, cell_bottom_right))

        new_y = 0
        for row in self._cells:
            new_x = 0
            for cell in row:
                cell.top_left = Point(
                        cell._x1 + new_x,
                        cell._y1 + new_y
                )
                cell.bottom_right = Point(
                        cell.top_left.x + self.cell_size_x,
                        cell.top_left.y + self.cell_size_y
                )
                new_x += self.cell_size_x
                cell.update()
            new_y += self.cell_size_y

    def _draw_cell(self):#, i, j):
        #self.maze_size = Point(j, i)
        self._animate()

    def _animate(self):
        #maze = Cell(self.offset, self.maze_size + self.offset)
        #self.win.draw_cell(maze, "black")
        self.win.redraw()
        self.print_cells()

    def print_cells(self):
        for row in self._cells:
            for cell in row:
                self.win.draw_cell(cell, "black")
                self.win.redraw()
                time.sleep(0.01)
        self._break_entrance_and_exit()

    def _break_entrance_and_exit(self):
        first_cell = self._cells[0][0]
        first_cell.has_top_wall = False
        first_cell.draw(self.win.canvas)

        last_cell = self._cells[-1][-1]
        last_cell.has_bottom_wall = False
        last_cell.draw(self.win.canvas)

    def _break_walls_r(self, i, j):
        self._break_entrance_and_exit()
        current_cell = self._cells[i][j]
        current_cell.visited = True
        left_cell = None
        right_cell = None
        top_cell = None
        bottom_cell = None
        if i > 0:
            top_cell = self._cells[i-1][j]
        if i < self.num_rows-1:
            bottom_cell = self._cells[i+1][j]
        if j > 0:
            left_cell = self._cells[i][j-1]
        if j < self.num_cols-1:
            right_cell = self._cells[i][j+1]

        while True:
            to_visit = []
            if top_cell and not top_cell.visited:
                to_visit.append((top_cell, i-1, j, "top"))
                print(f"Can go left from ({i}, {j}) to ({i-1}, {j})")
            if bottom_cell and not bottom_cell.visited:
                to_visit.append((bottom_cell, i+1, j, "bottom"))
                print(f"Can go right from ({i}, {j}) to ({i+1}, {j})")
            if left_cell and not left_cell.visited:
                to_visit.append((left_cell, i, j-1, "left"))
                print(f"Can go up from ({i}, {j}) to ({i}, {j-1})")
            if right_cell and not right_cell.visited:
                to_visit.append((right_cell, i, j+1, "right"))
                print(f"Can go bottom from ({i}, {j}) to ({i}, {j+1})")

            if len(to_visit) == 0:
                return

            choice = random.choice(to_visit)
            next_cell = choice[0]
            next_i = choice[1]
            next_j = choice[2]
            direction = choice[3]
            print(f"Chose direction: {direction} from ({i}, {j}) to ({next_i}, {next_j})")

            if direction == "left":
                print(f"Breaking left wall from ({i}, {j}) to ({next_i}, {next_j})")
                current_cell.has_left_wall = False
                next_cell.has_right_wall = False
            elif direction == "right":
                print(f"Breaking right wall at ({i}, {j}) to ({next_i}, {next_j})")
                current_cell.has_right_wall = False
                next_cell.has_left_wall = False
            elif direction == "top":
                print(f"Breaking top wall at ({i}, {j}) to ({next_i}, {next_j})")
                current_cell.has_top_wall = False
                next_cell.has_bottom_wall = False
            elif direction == "bottom":
                print(f"Breaking bottom wall at ({i}, {j}) to ({next_i}, {next_j})")
                current_cell.has_bottom_wall = False
                next_cell.has_top_wall = False
            print(current_cell.cell_walls())
            print(next_cell.cell_walls())

            current_cell.draw(self.win.canvas)
            next_cell.draw(self.win.canvas)
            time.sleep(0.05)
            self.win.redraw()
            self._break_walls_r(next_i, next_j)
