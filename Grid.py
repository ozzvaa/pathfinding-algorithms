import math
from enum import Enum


class State(Enum):
    UNEXPLORED = "gray79"
    OPEN = "seagreen1"
    CLOSED = "red3"
    OBSTACLE = "gray28"
    START = "springgreen2"
    FINISH = "orangered"


class Cell:
    def __init__(self, row, col, value=None, grid=None):
        self.row = row
        self.col = col
        self.value = value
        self.grid: Grid = grid
        self.parent: Cell = None
        self.state: State = State.UNEXPLORED
        self.g_cost : float = float("inf") # Start to cell
        self.h_cost : float = 0 # Heuristic score - goal to cell
        self._f_cost : float = 0 # full score - g + h

    def __repr__(self):
        return f"(row:{self.row}, col:{self.col}, value:{self.value})"

    def __str__(self):
        return f"({self.row},{self.col},{self.state.name})"

    def __eq__(self, other):
        return self.value == other.value and self.row == other.row and self.col == other.col

    def __lt__(self, other: "Cell"):
        return self.h_cost < other.h_cost

    def __hash__(self):
        return hash((self.row, self.col, self.value))

    @property
    def f_cost(self):
        self.calc_score()
        return self._f_cost

    def get_neighbors(self) -> list["Cell"]:
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        neighbors = []
        for dy, dx in directions:
            cell = self.grid[self.row + dy, self.col + dx]
            if cell is not None:
                neighbors.append(cell)
        return neighbors

    def calc_score(self):
        self._f_cost = self.g_cost + self.h_cost

    def dist_to(self, other: "Cell") -> int:
        dx = self.col - other.col
        dy = self.row - other.row
        distance = int(math.sqrt(dx*dx + dy*dy) * 10+0.5)
        return distance


    # def open_cell(self):
    #     if self.state == State.UNEXPLORED:
    #         self.state: State = State.CLOSED
    #         self.calc_score()
    #
    #     for n in self.get_neighbors():
    #         if n.state == State.UNEXPLORED:
    #             n.state = State.OPEN
    #             n.calc_score()




class Grid:
    def __init__(self, rows = 10, cols = 10):
        self.rows: int = rows
        self.cols: int = cols
        self.grid: list[list["Cell"]] = [[Cell(row, col, value=row*self.cols + col, grid=self) for col in range(self.cols)] for row in range(self.rows)]
        self.start: Cell = None
        self.finish: Cell = None

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

    def set_start(self, start: Cell):
        if self.start is not None:
            self.start.state = State.UNEXPLORED
        start.state = State.START
        self.start = start

    def set_finish(self, finish: Cell):
        if self.finish is not None:
            self.finish.state = State.UNEXPLORED
        finish.state = State.FINISH
        self.finish = finish

if __name__ == "__main__":
    grid = Grid(rows = 10, cols = 10)
    c = grid[2,3]
    print(c.get_neighbors())
