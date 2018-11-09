import os

import pygame

if os.name == 'posix':
    # Linux
    ROOTDIR = os.path.abspath(os.curdir).replace(';', '')
else:
    # Windows
    ROOTDIR = os.getcwd().replace(';', '')

IMGDIR = os.path.join(ROOTDIR, 'img')
LVLDIR = os.path.join(ROOTDIR, 'lvl')
RESDIR = os.path.join(ROOTDIR, 'res')

# Game Window variables
WWIDTH = 1056
WHEIGHT = 616

# Map dimensions
MAP_HEIGHT = 200
MAP_WIDTH = 200

# Image Variables
IMGSIZE = 16

# Surface
windowSurface = pygame.display.set_mode((WWIDTH, WHEIGHT), 0, 32)

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKWALL = (0, 0, 100)
DARKFLOOR = (50, 50, 150)

# Images
grass_image = pygame.image.load(os.path.join(IMGDIR, 'floor.bmp')).convert_alpha()
dirt_image = pygame.image.load(os.path.join(IMGDIR, 'water.bmp')).convert_alpha()
stone_image = pygame.image.load(os.path.join(IMGDIR, 'water.bmp')).convert_alpha()
water_image = pygame.image.load(os.path.join(IMGDIR, 'water.bmp')).convert_alpha()
images = {
    'grass': grass_image,
    'dirt': dirt_image,
    'stone': stone_image,
    'water': water_image
}
