import pygame

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

    def init_grid(self):
        pass



class GUI:
    def __init__(self):
        self.running = False
        pygame.init()

        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()



    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((0, 25, 120))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

