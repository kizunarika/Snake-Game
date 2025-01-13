from data import *
from random import randint


class Fruit:
    def __init__(self):
        self.apple = pygame.image.load("Graphics/Apple.png").convert_alpha()
        self.randomize()

    def draw_fruit(self, screen: pygame.Surface):
        fruit_rect = pygame.Rect(
            int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
        screen.blit(self.apple, fruit_rect)

    def randomize(self):
        self.pos = vector(randint(0, CELL_NUMBER - 1),
                          randint(0, CELL_NUMBER - 1))
