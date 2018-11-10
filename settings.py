import os

import pygame

import mylogger

logger = mylogger.setup_custom_logger('root')

logger.debug('settings.py loaded')

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
MAP_HEIGHT = 500
MAP_WIDTH = 500
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
logger.debug(f'Colors loaded')

# Images
logger.debug('Loading images...')
grass_image = pygame.image.load(os.path.join(IMGDIR, 'grass.bmp')).convert_alpha()
dirt_image = pygame.image.load(os.path.join(IMGDIR, 'dirt.bmp')).convert_alpha()
stone_image = pygame.image.load(os.path.join(IMGDIR, 'stone.bmp')).convert_alpha()
water_image = pygame.image.load(os.path.join(IMGDIR, 'water_0.bmp')).convert_alpha()
images = {
    'grass': grass_image,
    'dirt': dirt_image,
    'stone': stone_image,
    'water': water_image
}
logger.debug('Images loaded')
logger.debug(f'images = {str(images)}')
logger.debug('Settings loaded successfully')
