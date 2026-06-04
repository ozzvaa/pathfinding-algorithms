import time
from zoneinfo import reset_tzpath

import Cell
from Grid import Grid, Cell, State
import heapq

class Pathfinding:
    def __init__(self, grid: Grid, diagonals = True, delay = 0, use_heuristic=True, use_manhattan=True):
        self.grid = grid
        self.pause = False
        self.running = False
        self.solved = False
        self.path = []
        self.diagonals = diagonals
        self.delay = 0
        self.open_set = []
        self.closed_set = set()
        self.use_heuristic = use_heuristic
        self.use_manhattan = use_manhattan

        # Statistics
        self.execution_time = 0
        self.nodes_expanded = 0
        self.max_open_size = 0
        self.path_length = 0
        self.path_cost = 0
        
    def heuristic(self, current: Cell, use_heuristic = True, use_manhattan=True):
        if not use_heuristic:
            return 0 # Plain dijkstra
        # returns heuristic distance from cell to goal cell - A*
        return current.dist_to(self.grid.finish, use_manhattan)

    def run(self):
        start_time = time.perf_counter()
        self.running = True

        use_heuristic = self.use_heuristic
        use_manhattan = self.use_manhattan

        start = self.grid.start
        goal = self.grid.finish


        start.g_cost = 0
        start.h_cost = self.heuristic(start, use_heuristic, use_manhattan)
        start.calc_score()

        heapq.heappush(self.open_set, (start.f_cost, start))

        # Začneš pri prvem - min 0
        while self.open_set and self.running:
            while self.pause:
                pass
            # self.pause = True
            if self.delay:
                time.sleep(self.delay)
                if not self.running:
                    return

            _, current = heapq.heappop(self.open_set)
            if current in self.closed_set:
                continue

            self.nodes_expanded += 1
            self.closed_set.add(current)
            current.state = State.CLOSED

            if current == goal:
                self.execution_time = time.perf_counter() - start_time

                self.path_cost = current.g_cost
                self.reconstruct_path(goal)

                self.solved = True
                self.running = False
                return self.path

            # Odpreš vse sosede - izračunaš f, d, g
            for n in current.get_neighbors(d8=self.diagonals):
                if not self.running:
                    return

                if n in self.closed_set or n.state == State.OBSTACLE:
                    continue
                # time.sleep(0.1)

                opened_distance = current.g_cost + current.dist_to(n, use_manhattan)

                if opened_distance < n.g_cost:

                    n.parent = current
                    n.g_cost = opened_distance
                    n.h_cost = self.heuristic(n, use_heuristic, use_manhattan)
                    n.calc_score()

                    heapq.heappush(self.open_set, (n.f_cost, n))
                    self.max_open_size = max(
                        self.max_open_size,
                        len(self.open_set)
                    )

                    if n.state == State.UNEXPLORED:
                        n.state = State.OPEN
        self.running = False

    def reconstruct_path(self, goal: Cell):
        path_node = goal

        while path_node:
            self.path.append(path_node)
            path_node = path_node.parent

        self.path.reverse()

        self.path_length = len(self.path) - 1

        return self.path

    def get_stats(self):
        return {
            "execution_time": self.execution_time,
            "nodes_expanded": self.nodes_expanded,
            "path_length": self.path_length,
            "path_cost": self.path_cost,
            "max_open_size": self.max_open_size,
            "closed_size": len(self.closed_set)
        }

    def reset(self):
        self.running = False
        self.pause = False
        self.solved = False
        self.path = []
        self.open_set = []
        self.closed_set = set()
        self.execution_time = 0
        self.nodes_expanded = 0
        self.max_open_size = 0
        self.path_length = 0
        self.path_cost = 0


if __name__ == "__main__":
    grid = Grid()
    cell = grid[2,5]
    grid.set_start(grid[0,1])
    grid.set_finish(grid[8,7])

    alg = Pathfinding(grid)
    alg.run()

