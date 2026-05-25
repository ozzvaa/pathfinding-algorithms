class Cell:
    def __init__(self, row, col, value=None, grid=None):
        self.row = row
        self.col = col
        self.value = value
        self.grid: Grid = grid

    def __repr__(self):
        return f"(row:{self.row}, col:{self.col}, value:{self.value})"

    def __str__(self):
        return f"({self.row},{self.col},{self.value})"

class Grid:
    def __init__(self, rows = 10, cols = 10):
        self.rows = rows
        self.cols = cols
        self.grid = [[Cell(row, col, row*self.cols + col) for col in range(self.cols)] for row in range(self.rows)]


    def __str__(self):
        grid_str=""

        for row in range(self.rows):
            for col in range(self.cols):
                grid_str+=f"| {self.grid[row][col]} |"
            grid_str+="\n"
        return grid_str.replace("||","|")

if __name__ == "__main__":
    grid = Grid(rows = 10, cols = 10)
    print(grid)