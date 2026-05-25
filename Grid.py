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

    def __eq__(self, other):
        return self.value == other.value and self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash((self.row, self.col, self.value))

    def get_neighbors(self) -> list["Cell"]:
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 1)]
        neighbors = []
        for dy, dx in directions:
            cell = self.grid[self.row + dy, self.col + dx]
            if cell is not None:
                neighbors.append(cell)
        return neighbors

class Grid:
    def __init__(self, rows = 10, cols = 10):
        self.rows: int = rows
        self.cols: int = cols
        self.grid: list[list["Cell"]] = [[Cell(row, col, value=row*self.cols + col, grid=self) for col in range(self.cols)] for row in range(self.rows)]


    def __str__(self):
        grid_str=""

        for row in range(self.rows):
            for col in range(self.cols):
                grid_str+=f"| {self.grid[row][col]} |"
            grid_str+="\n"
        return grid_str.replace("||","|")

    def __getitem__(self, item) -> Cell | None:
        return self.get(*item)

    def get_by_index(self, index) -> Cell | None:
        row = index // self.cols
        col = index % self.cols
        return self.get(row, col)

    def get(self, row, col) -> Cell | None:
        if self.in_bounds(row, col):
            return self.grid[row][col]
        return None

    def in_bounds(self, row, col) -> bool:
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return True
        return False

if __name__ == "__main__":
    grid = Grid(rows = 10, cols = 10)
    c = grid[2,3]
    print(c.get_neighbors())
