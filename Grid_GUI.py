import pygame

from Grid import Grid, Cell

class Tile(pygame.Rect):
    def __init__(self, cell: Cell, size: int, offset_x: int = 0, offset_y: int = 0):
        self.cell = cell

        x = cell.col * size + offset_x
        y = cell.row * size + offset_y


        super().__init__(x, y, size, size)




class GUI:
    def __init__(self):
        self.running = False
        pygame.init()

        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.grid = Grid(rows = 50, cols = 50)

        screen_w, screen_h = self.screen.get_size()
        tile_size = min(screen_w // self.grid.cols, screen_h // self.grid.rows)

        grid_w = self.grid.cols * tile_size
        grid_h = self.grid.rows * tile_size

        offset_x = (screen_w - grid_w) // 2
        offset_y = (screen_h - grid_h) // 2

        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                self.grid.grid[row][col] = Tile(cell = Cell(row, col),
                                                size=tile_size,
                                                offset_x=offset_x,
                                                offset_y=offset_y)

    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((0, 25, 120))
            self.draw_grid()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def draw_grid(self):
        grid = self.grid

        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                tile: pygame.Rect = grid[row, col]
                pygame.draw.rect(self.screen, "gray", rect=tile,width=1)
