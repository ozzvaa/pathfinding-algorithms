import time

import pygame

from Grid import Grid, Cell, State
import threading
from SearchAlgorithms import Pathfinding


class Tile(Cell):
    def __init__(self, size: int, row, col, offset_x: int = 0, offset_y: int = 0):

        super().__init__(row, col)

        x = col * size + offset_x
        y = row * size + offset_y

        self.rect = pygame.Rect(x, y, size, size)




class GUI:
    def __init__(self, rows: int = 15, cols: int = 15):
        self.running = False
        pygame.init()
        self.font = pygame.font.SysFont("Arial", 12)
        self.font_settings = pygame.font.SysFont("consolas", 14)

        self.SIDEBAR_WIDTH  = 320
        self.screen = pygame.display.set_mode((800 + self.SIDEBAR_WIDTH, 600))
        self.clock = pygame.time.Clock()
        self.grid = Grid(rows = rows, cols = cols)

        self.offset_x = 0
        self.offset_y = 0
        self.tile_size = 0

        # Visual settings
        self.draw_parents = False
        self.draw_path = True
        self.draw_fcost = False
        self.delay_change_rate = 0.01
        allow_diagonals = True
        delay = 0
        manhattan = True



        self.init_grid()
        self.search_alg = Pathfinding(self.grid, allow_diagonals, delay, manhattan)
        self.alg_started = False

    def init_grid(self):
        screen_w, screen_h = self.screen.get_size()
        screen_w -= self.SIDEBAR_WIDTH
        self.tile_size = min(screen_w // self.grid.cols, screen_h // self.grid.rows)

        grid_w = self.grid.cols * self.tile_size
        grid_h = self.grid.rows * self.tile_size

        self.offset_x = (screen_w - grid_w) // 2
        self.offset_y = (screen_h - grid_h) // 2

        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                tile: Tile = Tile(row=row, col=col,
                                  size=self.tile_size,
                                  offset_x=self.offset_x,
                                  offset_y=self.offset_y)
                tile.grid = self.grid
                tile.g_cost = float("inf")
                tile.parent = None

                self.grid.grid[row][col] = tile
        self.grid.start = None
        self.grid.finish = None

    def reset_grid(self):
        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                tile = self.grid[row, col]
                tile.g_cost = float("inf")
                tile.parent = None
                if tile.state == State.OBSTACLE:
                    continue
                tile.state = State.UNEXPLORED




    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event)

                if event.type == pygame.KEYDOWN:
                    self.handle_key(event)

            self.screen.fill((0, 25, 120))
            self.draw_grid()
            self.draw_sidebar()

            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()

    def draw_grid(self):
        grid = self.grid


        tile_texts = []
        arrows = []
        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                tile: Tile = grid[row, col]
                # Tile drawing
                if tile.start:
                    tile_color = State.START.value
                elif tile.finish:
                    tile_color = State.FINISH.value
                else:
                    tile_color = tile.state.value
                pygame.draw.rect(self.screen, tile_color, rect=tile.rect)
                # Outline
                pygame.draw.rect(self.screen, "black", rect=tile.rect, width=1)
                # Font
                if self.draw_fcost and tile.state != State.UNEXPLORED:
                    text = self.font.render(f"{tile.f_cost:.2f}", True, (0, 0, 0))
                    text_pos = tile.rect.move(10, 10)
                    tile_texts.append((text, text_pos))

                if self.draw_parents and tile.parent is not None:
                    arrows.append(tile)

        # Drawing text
        for text, rect in tile_texts:
            self.screen.blit(text, rect)

        # Drawing arrows
        for tile in arrows:
            draw_arrow(self.screen, tile.rect, tile.parent.rect)

        # Drawing path back
        if self.search_alg.solved and self.search_alg.path:
            for node in self.search_alg.path:
                if node.parent:
                    draw_arrow(self.screen, node.parent.rect, node.rect, (0, 200, 0))

    def draw_sidebar(self):
        x = self.screen.get_width() - self.SIDEBAR_WIDTH
        h = self.screen.get_height()

        pygame.draw.rect(self.screen, (18, 18, 22), (x, 0, self.SIDEBAR_WIDTH, h))

        label_x = x + 12
        value_x = x + self.SIDEBAR_WIDTH - 12

        def draw_row(label, value="", y=0, color=(220, 220, 220), value_color=(200, 200, 200)):
            label_surf = self.font_settings.render(label, True, color)
            self.screen.blit(label_surf, (label_x, y))

            if value != "":
                value_surf = self.font_settings.render(value, True, value_color)
                rect = value_surf.get_rect()
                rect.topright = (value_x, y)
                self.screen.blit(value_surf, rect)

            return y + 20

        y = 15

        # TITLE
        title = self.font_settings.render("PATHFINDING VISUALIZER", True, (120, 200, 255))
        self.screen.blit(title, (label_x, y))
        y += 30

        # CONTROLS
        y = draw_row("CONTROLS", "", y, (180, 180, 180))
        y = draw_row("[LMB]", "set START", y)
        y = draw_row("[RMB]", "set FINISH", y)
        y = draw_row("[MMB]", "toggle OBSTACLE", y)
        y = draw_row("[SPACE]", "run/pause", y)
        y = draw_row("[R]", "reset", y)

        y += 10

        # SETTINGS
        y = draw_row("SETTINGS", "", y, (180, 180, 180))

        y = draw_row("[UP/DOWN] Delay", f"{self.search_alg.delay:.2f}", y)

        heuristic = "Manhattan" if self.search_alg.use_manhattan else "Euclidean"
        y = draw_row("[H] Heuristic", heuristic, y, value_color=(180, 220, 255))

        diag = "ON" if self.search_alg.diagonals else "OFF"
        y = draw_row("[D] Diagonals", diag, y, value_color=(255, 200, 120))

        run = "YES" if self.search_alg.running else "NO"
        y = draw_row("Running", run, y, value_color=(255, 120, 120 if self.search_alg.running else 120))

        sol = "YES" if self.search_alg.solved else "NO"
        y = draw_row("Solved", sol, y, value_color=(120, 255, 120))


    def handle_click(self, event: pygame.event.Event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        x, y = event.pos
        x -= self.offset_x
        y -= self.offset_y

        if x < 0 or y < 0:
            return

        col = x // self.tile_size
        row = y // self.tile_size

        if row >= self.grid.rows or col >= self.grid.cols:
            return

        tile: Tile = self.grid[row, col]

        print(f"Clicked tile: {tile} - {tile.g_cost, tile.h_cost, tile.f_cost}")

        if event.button == pygame.BUTTON_LEFT:
            if self.alg_started:
                self.search_alg.reset()
                self.reset_grid()
                self.alg_started = False
            self.grid.set_start(tile)
        elif event.button == pygame.BUTTON_RIGHT:
            if self.alg_started:
                self.search_alg.reset()
                self.reset_grid()
                self.alg_started = False
            self.grid.set_finish(tile)
        elif event.button == pygame.BUTTON_MIDDLE:
            if tile.start or tile.finish:
                pass
            elif tile.state == State.UNEXPLORED:
                tile.state = State.OBSTACLE
            elif tile.state == State.OBSTACLE:
                tile.state = State.UNEXPLORED



    def handle_key(self, event: pygame.event.Event):
        if event.key == pygame.K_r:
            self.search_alg.reset()
            self.reset_grid()

        if event.key == pygame.K_SPACE:
            self.alg_started = True
            if self.grid.start and self.grid.finish:
                self.reset_grid()
                self.search_alg.reset()
                alg_thread = threading.Thread(target=self.search_alg.run)
                alg_thread.start()
        if event.key == pygame.K_p:
            self.draw_parents = not self.draw_parents
        if event.key == pygame.K_i:
            self.draw_fcost = not self.draw_fcost
        if event.key == pygame.K_d:
            self.search_alg.diagonals = not self.search_alg.diagonals
        if event.key == pygame.K_UP:
            self.search_alg.delay += self.delay_change_rate
        if event.key == pygame.K_DOWN:
            self.search_alg.delay -= self.delay_change_rate if self.search_alg.delay > self.delay_change_rate else 0
        if event.key == pygame.K_h:
            self.search_alg.use_manhattan = not self.search_alg.use_manhattan
import math

def draw_arrow(surface, start_rect, end_rect, color=(255, 0, 0)):
    start = start_rect.center
    end = end_rect.center

    pygame.draw.line(surface, color, start, end, 2)

    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    arrow_size = 10

    left = (
        end[0] - arrow_size * math.cos(angle - math.pi / 6),
        end[1] - arrow_size * math.sin(angle - math.pi / 6),
    )
    right = (
        end[0] - arrow_size * math.cos(angle + math.pi / 6),
        end[1] - arrow_size * math.sin(angle + math.pi / 6),
    )

    pygame.draw.polygon(surface, color, [end, left, right])


if __name__ == "__main__":
    gui = GUI()
    gui.run()