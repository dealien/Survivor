"""
.. module:: map
   :platform: Unix, Windows
   :synopsis: Contains required classes and functions for ``mapgen``.

.. moduleauthor:: Vyren

"""
import random

import pygame

import mapgen
import mylogger
from settings import IMGSIZE, ROTATING, IMPASSABLE, LOGLEVEL

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
        self.terrain = mapgen.generate_terrain(self.height, self.width, 4,
                                               {
                                                   '*': 0.4,
                                                   " ": 1,
                                                   "+": 0.75,
                                                   "#": 0.45
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


class Tile:
    """
    Holds information about a specific tile on the map.
    """

    def __init__(self, material, image, x, y):
        """
        :param material: The name of the material
        :param image: The name of the image to be used when rendering the tile
        :param x: The x position on the map
        :param y: The y position on the map
        """
        self.material = material
        # Rotate the texture if necessary
        if material in ROTATING:
            self.rot = random.randint(0, 3) * 90
            self.texture = pygame.transform.rotate(image, self.rot)
        else:
            self.rot = 0
            self.texture = image
        self.collisions = False
        self.passable = self.material not in IMPASSABLE
        self.durability = -1
        self.rect = pygame.Rect(x, y, IMGSIZE, IMGSIZE)

    def __str__(self):
        return f'{self.material} tile at [{self.rect[0]}, {self.rect[1]}]'
