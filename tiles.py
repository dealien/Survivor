import os
import pprint

import pygame

import mylogger
from settings import IMGDIR

pp = pprint.PrettyPrinter(indent=4)

logger = mylogger.setup_custom_logger('root')

logger.debug('Loading tiles...')


# Tiles
class Tile:
    """Tiles hold information about each point on the map, and
    are used to generate a tileset.
    """

    def __init__(self, image, material, collisions, durability):
        self.image = image
        self.material = material
        self.collisions = collisions
        self.durability = durability


tiles = {
    'dirt': Tile(pygame.image.load(os.path.join(IMGDIR, 'dirt.bmp')).convert_alpha(), 'grass', False, -1),
    'grass': Tile(pygame.image.load(os.path.join(IMGDIR, 'grass.bmp')).convert_alpha(), 'dirt', False, -1),
    'stone': Tile(pygame.image.load(os.path.join(IMGDIR, 'stone.bmp')).convert_alpha(), "stone", True, -1),
    'water': Tile(pygame.image.load(os.path.join(IMGDIR, 'water_0.bmp')).convert_alpha(), 'water', False, -1)
}
logger.debug('Tiles loaded')
logger.debug(pp.pprint(tiles))
