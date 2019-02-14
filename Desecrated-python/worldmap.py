import pygame
import math

class WorldMap:
	tiles={}

	def add_tile(self,tile):
		self.tiles[tile.location]=tile

	def draw(self,surface):
		for tile in self.tiles:
			tile.draw()


class Tile(object):
    terrain_type=None
    location=(100,100)

    def gen_hexagon(self,center,r):
    	h=r*math.sqrt(3)/2
    	x,y=center

    	return [
    		(x+.5*r,y+h),
    		(x+r,y),
    		(x+.5*r,y-h),
    		(x-.5*r,y-h),
    		(x-r,y),
    		(x-.5*r,y+h)
    	]

    def draw(self, surface):
        # pygame.draw.rect(surface, pygame.Color(0, 0, 0), pygame.rect.Rect(x, y, w, h))
        hexagon=self.gen_hexagon(self.location,30)
        pygame.draw.polygon(surface, pygame.Color(0, 0, 200), hexagon, 0)
        # pygame.draw.circle(surface, pygame.Color(0, 0, 200), self.location, 30)