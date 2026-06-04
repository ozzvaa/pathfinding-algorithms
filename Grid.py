import math
from enum import Enum
import json

class State(Enum):
    UNEXPLORED = "#e0e0e0"   # light gray (neutral, unvisited)
    OPEN        = "#4da3ff"   # blue (frontier / candidates)
    CLOSED      = "#ff6b6b"   # red (already processed)
    OBSTACLE    = "#2b2b2b"   # dark gray/near black (blocked)

    START       = "#2ecc71"   # green (origin)
    FINISH      = "#e74c3c"   # strong red (goal)

class Cell:
    def __init__(self, row, col, value=None, grid=None, state=State.UNEXPLORED):
        self.row = row
        self.col = col
        self.value = value
        self.grid: Grid = grid
        self.parent: Cell = None
        self.state: State = State.UNEXPLORED
        self.g_cost : float = float("inf") # Start to cell
        self.h_cost : float = 0 # Heuristic score - goal to cell
        self._f_cost : float = 0 # full score - g + h
        self.start = False
        self.finish = False


    def __repr__(self):
        return f"(row:{self.row}, col:{self.col}, value:{self.value})"

    def __str__(self):
        return f"({self.row},{self.col},{self.state.name})"

    def __eq__(self, other):
        return self.value == other.value and self.row == other.row and self.col == other.col

    def __lt__(self, other: "Cell"):
        if self.f_cost == other.f_cost:
            return self.h_cost < other.h_cost  # tiebreak: prefer closer to goal
        return self.f_cost < other.f_cost

    def __hash__(self):
        return hash((self.row, self.col, self.value))

    @property
    def f_cost(self):
        self.calc_score()
        return self._f_cost

    def get_neighbors(self, d8 = True) -> list["Cell"]:
        if d8:
            directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        else:
            directions = [(-1,0), (0, -1), (0, 1), (1, 0)]
        neighbors = []
        for dy, dx in directions:
            cell = self.grid[self.row + dy, self.col + dx]
            if cell is not None:
                neighbors.append(cell)
        return neighbors

    def calc_score(self):
        self._f_cost = self.g_cost + self.h_cost

    def dist_to(self, other: "Cell", manhattan=True) -> int:
        dx = self.col - other.col
        dy = self.row - other.row
        # distance = (math.sqrt(dx*dx + dy*dy))
        if manhattan:
            distance = abs(dx) + abs(dy) # Manhattan distance
        else:
            distance = math.sqrt(dx**2 + dy**2) # Eucilidian
        return distance





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

    def to_dict(self) -> dict:
        return {
            "rows": self.rows,
            "cols": self.cols,
            "start": (self.start.row, self.start.col) if self.start else None,
            "finish": (self.finish.row, self.finish.col) if self.finish else None,
            "cells": [
                {
                    "row": cell.row,
                    "col": cell.col,
                    "value": cell.value,
                    "state": cell.state.name,
                    "g_cost": cell.g_cost,
                    "h_cost": cell.h_cost,
                    "start": cell.start,
                    "finish": cell.finish,
                }
                for row in self.grid
                for cell in row
            ]
        }

    def save_json(self, path: str):
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def from_dict(cls, data: dict) -> "Grid":
        grid = cls(rows=data["rows"], cols=data["cols"])

        # rebuild cells
        for cell_data in data["cells"]:
            r, c = cell_data["row"], cell_data["col"]
            cell = grid.grid[r][c]

            cell.value = cell_data["value"]
            cell.state = State[cell_data["state"]]
            cell.g_cost = float("inf")
            cell.h_cost = 0
            cell.start = cell_data.get("start", False)
            cell.finish = cell_data.get("finish", False)

        # restore start/finish pointers
        if data.get("start"):
            r, c = data["start"]
            grid.start = grid.grid[r][c]

        if data.get("finish"):
            r, c = data["finish"]
            grid.finish = grid.grid[r][c]

        return grid

    @classmethod
    def load_json(cls, path: str) -> "Grid":
        with open(path, "r") as f:
            data = json.load(f)
        return cls.from_dict(data)

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

    def set_start(self, start_cell: Cell):
        if self.start is not None:
            self.start.state = State.UNEXPLORED
            self.start.start = False
        start_cell.start = True
        start_cell.finish = False
        start_cell.state = State.UNEXPLORED
        self.start = start_cell

    def set_finish(self, finish_cell: Cell):
        if self.finish is not None:
            self.finish.state = State.UNEXPLORED
            self.finish.finish = False
        finish_cell.finish = True
        finish_cell.start = False
        finish_cell.state = State.UNEXPLORED
        self.finish = finish_cell

if __name__ == "__main__":
    grid = Grid(rows = 10, cols = 10)
    c = grid[2,3]
    print(c.get_neighbors())
