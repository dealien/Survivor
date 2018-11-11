import mapgen

import mylogger
from tiles import tiles

logger = mylogger.setup_custom_logger('root')


class Map:
    """The map object. Input the width, height, and smoothness.
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
                                                   '*': tiles['water'],
                                                   " ": tiles['grass'],
                                                   "+": tiles['dirt'],
                                                   "#": tiles['stone']
                                               })
        logger.debug('Map generated (height=%d, width=%d, smoothness=%d)' % (self.height, self.width, self.smoothness))

    def __repr__(self):
        return self.terrain

    def __str__(self):
        return str(self.terrain)
