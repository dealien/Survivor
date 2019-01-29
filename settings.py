import os
import pprint

import pygame

import mylogger

logger = mylogger.setup_custom_logger('root')
pp = pprint.PrettyPrinter(indent=4)

logger.debug('Loading settings...')

if os.name == 'posix':
    # Linux
    ROOTDIR = os.path.abspath(os.curdir).replace(';', '')
else:
    # Windows
    ROOTDIR = os.getcwd().replace(';', '')

ADIR = os.path.join(ROOTDIR, 'assets')
IMGDIR = os.path.join(ADIR, 'images')
AUDDIR = os.path.join(ADIR, 'sound')
logger.debug(f'ROOTDIR = {ROOTDIR}')
logger.debug(f'ADIR = {ADIR}')
logger.debug(f'IMGDIR = {IMGDIR}')
logger.debug(f'AUDDIR = {AUDDIR}')

# Constants
# Directions
NORTH = 'NORTH'
WEST = 'WEST'
SOUTH = 'SOUTH'
EAST = 'EAST'

# Game Window variables
WINDOW_WIDTH = 1056
WINDOW_HEIGHT = 616
logger.debug(f'WINDOW_WIDTH = {WINDOW_WIDTH}')
logger.debug(f'WINDOW_HEIGHT = {WINDOW_HEIGHT}')

# Mapgen settings
MAP_HEIGHT = 150
MAP_WIDTH = 150
MAP_SMOOTHNESS = 10
logger.debug(f'MAP_HEIGHT = {MAP_HEIGHT}')
logger.debug(f'MAP_HEIGHT = {MAP_HEIGHT}')

# Image Variables
IMGSIZE = 16
logger.debug(f'IMGSIZE = {IMGSIZE}')

# Surface
windowSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)

# Colors
logger.debug('Loading colors...')
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKWALL = (0, 0, 100)
DARKFLOOR = (50, 50, 150)
logger.debug('Colors loaded')

# Textures
logger.debug('Loading graphics...')
GRAPHICS = {}
directory = os.fsencode(IMGDIR)
dirs = [name for name in os.listdir(IMGDIR) if os.path.isdir(os.path.join(IMGDIR, name))]
for directory in dirs:
    for file in os.listdir(os.path.join(IMGDIR, directory)):
        filename = os.fsdecode(file)
        if filename.endswith('.bmp') or filename.endswith('.png'):
            GRAPHICS[filename[:-4]] = pygame.image.load(os.path.join(IMGDIR, directory, filename)).convert_alpha()
            continue
        else:
            continue
logger.debug('Textures loaded')
logger.debug('GRAPHICS = \n' + pp.pformat(GRAPHICS))

# Tiles
# Tiles whose textures should rotate
ROTATING = ['grass']
# Tiles that cannot be moved through
IMPASSABLE = ['water']

logger.debug('Settings loaded successfully')
