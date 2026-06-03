import time
from zoneinfo import reset_tzpath

import Cell
from Grid import Grid, Cell, State
import heapq

class A_star:
    def __init__(self, grid: Grid, diagonals = True, delay = 0):
        self.grid = grid
        self.pause = False
        self.running = False
        self.solved = False
        self.path = []
        self.diagonals = diagonals
        self.delay = 0
        self.open_set = []
        self.closed_set = set()
        
    def heuristic(self, current: Cell):
        # returns heuristic distance from cell to goal cel
        return current.dist_to(self.grid.finish)

    def run(self):
        self.running = True
        start = self.grid.start
        goal = self.grid.finish


        start.g_cost = 0
        start.h_cost = self.heuristic(start)
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

            self.closed_set.add(current)
            current.state = State.CLOSED

            if current == goal:
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

                opened_distance = current.g_cost + current.dist_to(n)

                if opened_distance < n.g_cost:

                    n.parent = current
                    n.g_cost = opened_distance
                    n.h_cost = self.heuristic(n)
                    n.calc_score()

                    heapq.heappush(self.open_set, (n.f_cost, n))

                    if n.state == State.UNEXPLORED:
                        n.state = State.OPEN

    def reconstruct_path(self, goal: Cell):
        path_node = goal
        while path_node:
            self.path.append(path_node)
            path_node = path_node.parent
        return self.path

    def reset(self):
        self.running = False
        self.pause = False
        self.solved = False
        self.path = []
        self.open_set = []
        self.closed_set = set()


if __name__ == "__main__":
    grid = Grid()
    cell = grid[2,5]
    grid.set_start(grid[0,1])
    grid.set_finish(grid[8,7])

    alg = A_star(grid)
    alg.run()

