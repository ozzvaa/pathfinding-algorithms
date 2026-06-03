import pygame

from Grid import Grid, Cell
import threading
from SearchAlgorithms import A_star


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

        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.grid = Grid(rows = rows, cols = cols)

        self.offset_x = 0
        self.offset_y = 0
        self.tile_size = 0

        self.reset_grid()
        self.a_star = A_star(self.grid)
        self.changed = False

    def reset_grid(self):
        screen_w, screen_h = self.screen.get_size()
        self.tile_size = min(screen_w // self.grid.cols, screen_h // self.grid.rows)

        grid_w = self.grid.cols * self.tile_size
        grid_h = self.grid.rows * self.tile_size

        self.offset_x = (screen_w - grid_w) // 2
        self.offset_y = (screen_h - grid_h) // 2

        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                tile : Tile = Tile(row=row, col=col,
                                     size=self.tile_size,
                                     offset_x=self.offset_x,
                                     offset_y=self.offset_y)
                tile.grid = self.grid
                tile.g_cost = float("inf")
                tile.parent = None

                self.grid.grid[row][col] = tile
        self.grid.start = None
        self.grid.finish = None


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
                pygame.draw.rect(self.screen, tile.state.value, rect=tile.rect)
                # Outline
                pygame.draw.rect(self.screen, "black", rect=tile.rect, width=1)
                # Font
                text = self.font.render(f"{tile.f_cost:.2f}", True, (0, 0, 0))
                text_pos = tile.rect.move(10, 10)
                tile_texts.append((text, text_pos))

                if tile.parent is not None:
                    arrows.append(tile)

        # Drawing text
        for text, rect in tile_texts:
            self.screen.blit(text, rect)

        # Drawing arrows
        # for tile in arrows:
        #     draw_arrow(self.screen, tile.rect, tile.parent.rect)

        # Drawing path back
        if self.a_star.solved and self.a_star.path:
            for node in self.a_star.path:
                if node.parent:
                    draw_arrow(self.screen, node.parent.rect, node.rect, (0, 200, 0))


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
            if self.changed:
                self.a_star.reset()
                self.reset_grid()
                self.changed = False
            self.grid.set_start(tile)
        elif event.button == pygame.BUTTON_RIGHT:
            if self.changed:
                self.a_star.reset()
                self.reset_grid()
                self.changed = False
            self.grid.set_finish(tile)

    def handle_key(self, event: pygame.event.Event):
        if event.key == pygame.K_r:
            self.a_star.reset()
            self.reset_grid()

        if event.key == pygame.K_SPACE:
            self.changed = True
            if self.grid.start and self.grid.finish:
                if self.a_star.running:
                    self.a_star.pause = not self.a_star.pause
                else:
                    alg_thread = threading.Thread(target=self.a_star.run)
                    alg_thread.start()

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