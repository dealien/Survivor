"""
.. module:: map
   :platform: Unix, Windows
   :synopsis: Contains required classes and functions for ``mapgen``.

.. moduleauthor:: Vyren

"""

import mapgen
import mylogger
from settings import LOGLEVEL

logger = mylogger.setup_custom_logger('root', LOGLEVEL)


class Map:
    """
    Stores information about the map, including terrain,
    tilemap, and the arguments used to generate the map.
    
    Uses ``mapgen.generate_terrain()`` to generate terrain and
    ``mapgen.generate_tilemap()`` to generate the tilemap.

    """

    def __init__(self, height, width, smoothness):
        """
        :param height: Height of map to generate
        :param width: Width of map to generate
        :param smoothness: Number of times the terrain should be smoothed
        """
        self.height = height
        self.width = width
        self.smoothness = smoothness
        self.key = {
            '*': 'water',
            " ": 'grass',
            "+": 'dirt',
            "#": 'stone'
        }
        self.terrain = mapgen.generate_terrain(self.height, self.width, self.smoothness,
                                               {
                                                   '*': 0.4,
                                                   " ": 1,
                                                   "+": 0.75,
                                                   "#": 0.45
                                               })
        self.tilemap = mapgen.generate_tilemap(self.terrain, self.key)
        self.objectmap = mapgen.generate_objectmap(self.terrain, self.key)
        logger.debug('Map generated (height=%d, width=%d, smoothness=%d)' % (self.height, self.width, self.smoothness))

    def __repr__(self):
        return self.terrain

    def __str__(self):
        return str(self.terrain)
