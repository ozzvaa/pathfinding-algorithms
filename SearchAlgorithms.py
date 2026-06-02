import time
from zoneinfo import reset_tzpath

import Cell
from Grid import Grid, Cell, State
import heapq

class A_star:
    def __init__(self, grid: Grid):
        self.grid = grid

    def heuristic(self, current: Cell):
        # returns heuristic distance from cell to goal cel
        return current.dist_to(self.grid.finish)

    def run(self):
        start = self.grid.start
        goal = self.grid.finish
        open_set = []
        closed_set = set()

        start.g_cost = 0
        start.h_cost = self.heuristic(start)
        start.calc_score()

        heapq.heappush(open_set, (start.f_cost, start))

        # Začneš pri prvem - min 0
        while open_set:
            time.sleep(0.1)

            _, current = heapq.heappop(open_set)
            if current == goal:
                return "DONE"

            closed_set.add(current)
            current.state = State.CLOSED

            # Odpreš vse sosede - izračunaš f, d, g
            for n in current.get_neighbors():

                if n in closed_set:
                    continue

                opened_distance = current.g_cost + current.dist_to(n)

                if opened_distance < n.g_cost:

                    n.parent = current
                    n.g_cost = opened_distance
                    n.h_cost = self.heuristic(n)
                    n.calc_score()

                    heapq.heappush(open_set, (n.f_cost, n))

                    n.state = State.OPEN if n.state == State.UNEXPLORED or n.state == State.OPEN else n.state







if __name__ == "__main__":
    grid = Grid()
    cell = grid[2,5]
    grid.set_start(grid[0,1])
    grid.set_finish(grid[8,7])

    alg = A_star(grid)
    alg.run()

