from tkinter import Tk, BOTH, Canvas

class Window():
    def __init__(self, width, height, title=None):
        self.width = width
        self.height = height
        self.root_widget = Tk()
        self.root_widget.title = title
        self.root_widget.protocol("WM_DELETE_WINDOW", self.close)
        self.canvas = Canvas()
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

    def draw(self, canvas, fill_color):
        if self.has_left_wall:
            left_wall = Line(self.top_left, Point(self.top_left.x, self.bottom_right.y))
            left_wall.draw(canvas, fill_color)
        if self.has_right_wall:
            right_wall = Line(Point(self.bottom_right.x, self.top_left.y), self.bottom_right)
            right_wall.draw(canvas, fill_color)
        if self.has_top_wall:
            top_wall = Line(self.top_left, Point(self.bottom_right.x, self.top_left.y))
            top_wall.draw(canvas, fill_color)
        if self.has_bottom_wall:
            bottom_wall = Line(Point(self.top_left.x, self.bottom_right.y), self.bottom_right)
            bottom_wall.draw(canvas, fill_color)

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
        self.maze_size = None #created with _draw_cell()
        self._cells = []
        self._create_cells()

    def _create_cells(self):
        for i in range(self.num_cols):
            self._cells.append([])
        cell_top_left = self.offset
        cell_bottom_right = self.offset
        for cell in self._cells:
            for i in range(self.num_rows):
                cell.append(Cell(cell_top_left, cell_bottom_right))

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
                        cell.top_left.y + self.cell_size_x
                )
                new_x += self.cell_size_x
                cell.update()
            new_y += self.cell_size_y

    def _draw_cell(self, i, j):
        self.maze_size = Point(j, i)
        self._animate()

    def _animate(self):
        maze = Cell(self.offset, self.maze_size + self.offset)
        self.win.draw_cell(maze, "black")
        self.win.redraw()
        self.print_cells()

    def print_cells(self):
        import time
        for row in self._cells:
            for cell in row:
                self.win.draw_cell(cell, "black")
                self.win.redraw()
                time.sleep(0.01)
        self.win.wait_for_close()
