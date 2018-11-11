import pygame

import mapgen
import mylogger
from settings import IMGSIZE

logger = mylogger.setup_custom_logger('root')


class Map:
    """Stores information about the map, including terrain,
    tilemap, and properties used to generate the map.
    Uses mapgen.generate_terrain() and
    mapgen.generate_tilemap() to generate terrain and tilemap.

    Input the height, width, and smoothness.
    """

    def __init__(self, height, width, smoothness):
        self.height = height
        self.width = width
        self.smoothness = smoothness
        self.terrain = mapgen.generate_terrain(self.height, self.width, 4,
                                               {
                                                   '*': .2,
                                                   " ": 1,
                                                   "+": 0.55,
                                                   "#": 0.25
                                               })
        self.tilemap = mapgen.generate_tilemap(self.terrain, {
            '*': 'water',
            " ": 'grass',
            "+": 'dirt',
            "#": 'stone'
        })
        logger.debug('Map generated (height=%d, width=%d, smoothness=%d)' % (self.height, self.width, self.smoothness))

    def __repr__(self):
        return self.terrain

    def __str__(self):
        return str(self.terrain)


# Tiles
class Tile:
    """Holds information about a specific map tile.
    """

    def __init__(self, material, image, x, y):
        self.material = material
        self.texture = image
        self.collisions = False
        self.durability = -1
        self.rect = pygame.Rect(x, y, IMGSIZE, IMGSIZE)
