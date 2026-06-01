import pygame

from Grid import Grid, Cell

class Tile(Cell):
    def __init__(self, size: int, row, col, offset_x: int = 0, offset_y: int = 0):

        super().__init__(row, col)

        x = col * size + offset_x
        y = row * size + offset_y

        self.rect = pygame.Rect(x, y, size, size)




class GUI:
    def __init__(self, rows: int = 50, cols: int = 50):
        self.running = False
        pygame.init()

        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.grid = Grid(rows = rows, cols = cols)

        screen_w, screen_h = self.screen.get_size()
        tile_size = min(screen_w // self.grid.cols, screen_h // self.grid.rows)

        grid_w = self.grid.cols * tile_size
        grid_h = self.grid.rows * tile_size

        offset_x = (screen_w - grid_w) // 2
        offset_y = (screen_h - grid_h) // 2

        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                tile : Tile = Tile(row=row, col=col,
                                     size=tile_size,
                                     offset_x=offset_x,
                                     offset_y=offset_y)
                tile.grid = self.grid
                self.grid.grid[row][col] = tile




    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event)

            self.screen.fill((0, 25, 120))
            self.draw_grid()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def draw_grid(self):
        grid = self.grid

        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                tile: Tile = grid[row, col]
                pygame.draw.rect(self.screen, tile.state.value, rect=tile.rect)
                pygame.draw.rect(self.screen, "black", rect=tile.rect, width=1)

    def handle_click(self, event: pygame.event.Event):
        mouse_pos = event.pos
        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                tile: Tile = self.grid[row, col]

                if tile.rect.collidepoint(mouse_pos):
                    print(f"Clicked tile: ({tile.row}, {tile.col})")
                    tile.open_tile()

if __name__ == "__main__":
    gui = GUI()
    gui.run()