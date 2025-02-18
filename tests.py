import unittest
from maze import Maze, Window

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        win = Window(400, 400)
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, win)
        self.assertEqual(
                len(m1._cells),
                num_rows,
        )
        self.assertEqual(
                len(m1._cells[0]),
                num_cols,
        )
    
    def test_visited_cells_reset(self):
        num_cols = 12
        num_rows = 10
        win = Window(400, 400)
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, win)
        m1._break_walls_r(0, 0)
        m1._reset_cells_visited()
        for row in m1._cells:
            for cell in row:
                if cell.visited:
                    return False
        return True

if __name__ == "__main__":
    unittest.main()
