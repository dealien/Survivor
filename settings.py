import os

import pygame

import mylogger

logger = mylogger.setup_custom_logger('root')

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

# Game Window variables
WINDOW_WIDTH = 1056
WINDOW_HEIGHT = 616
logger.debug(f'WINDOW_WIDTH = {WINDOW_WIDTH}')
logger.debug(f'WINDOW_HEIGHT = {WINDOW_HEIGHT}')

# Mapgen settings
MAP_HEIGHT = 50
MAP_WIDTH = 50
MAP_SMOOTHNESS = 10
logger.debug(f'MAP_HEIGHT = {MAP_HEIGHT}')
logger.debug(f'MAP_HEIGHT = {MAP_HEIGHT}')

# Image Variables
IMGSIZE = 16
logger.debug(f'IMGSIZE = {IMGSIZE}')

# Surface
windowSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)

# colors
logger.debug('Loading colors...')
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKWALL = (0, 0, 100)
DARKFLOOR = (50, 50, 150)
logger.debug('Colors loaded')
logger.debug('Settings loaded successfully')
