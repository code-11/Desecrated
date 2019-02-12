import pygame
import sys
from pygame.locals import *




def pygame_main_loop():
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((400, 300))

    herp=Tile()
    derp=TilePainter(DISPLAYSURF)
    
    pygame.display.set_caption('Hello World!')
    while True:  # main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        derp.draw_tile(herp)
        pygame.display.update()

class Tile(object):
    terrain_type=None
    location=(100,100)

    def draw(self, surface):
        # pygame.draw.rect(surface, pygame.Color(0, 0, 0), pygame.rect.Rect(x, y, w, h))
        pygame.draw.circle(surface, pygame.Color(0, 0, 200), self.location, 30)


class TilePainter(object):
    surface=None

    def __init__(self,surface):
        self.surface=surface

    def draw_tile(self,tile):
        tile.draw(self.surface)

if __name__ == "__main__":
    pygame_main_loop()