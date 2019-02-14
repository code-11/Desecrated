import pygame
import sys

from pygame.locals import *

import worldmap

def pygame_main_loop():
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((400, 300))

    herp = worldmap.WorldMap()
    derp = worldmap.Tile()
    herp.add_tile(derp)
    
    pygame.display.set_caption('Hello World!')
    while True:  # main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        derp.draw(DISPLAYSURF)
        pygame.display.update()

if __name__ == "__main__":
    pygame_main_loop()