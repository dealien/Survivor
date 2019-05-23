import os
import pprint

import pygame

import mylogger

LOGLEVEL = 3

main_log = open('main.log', 'w')
logger = mylogger.setup_custom_logger('root', LOGLEVEL)
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
AUDDIR = os.path.join(ADIR, 'sounds')
MUSDIR = os.path.join(ADIR, 'music')
logger.debug(f'ROOTDIR = {ROOTDIR}')
logger.debug(f'ADIR = {ADIR}')
logger.debug(f'IMGDIR = {IMGDIR}')
logger.debug(f'AUDDIR = {AUDDIR}')
logger.debug(f'MUSICDIR = {MUSDIR}')

# Constants
# Directions
NORTH = 'NORTH'
WEST = 'WEST'
SOUTH = 'SOUTH'
EAST = 'EAST'

# Game Window variables
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 900
logger.debug(f'WINDOW_WIDTH = {WINDOW_WIDTH}')
logger.debug(f'WINDOW_HEIGHT = {WINDOW_HEIGHT}')

# Mapgen settings
MAP_WIDTH = 50
MAP_HEIGHT = 50
MAP_SMOOTHNESS = 10
MAP_OBJECTPOP = 0.06
logger.debug(f'MAP_WIDTH = {MAP_WIDTH}')
logger.debug(f'MAP_HEIGHT = {MAP_HEIGHT}')
logger.debug(f'MAP_SMOOTHNESS = {MAP_SMOOTHNESS}')
logger.debug(f'MAP_OBJECTPOP = {MAP_OBJECTPOP}')

# Image Variables
IMGSIZE = 16
logger.debug(f'IMGSIZE = {IMGSIZE}')

# Surface
# Allows the program to continue running on headless platforms
try:
    windowSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
except pygame.error as e:
    logger.error(e)
    logger.warning('Running with dummy display.')
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    windowSurface = pygame.display.set_mode((1, 1))

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
for file in os.listdir(IMGDIR):
    filename = os.fsdecode(file)
    if filename.endswith('.bmp') or filename.endswith('.png'):
        GRAPHICS[filename[:-4]] = pygame.image.load(os.path.join(IMGDIR, filename)).convert_alpha()
        continue
    else:
        continue
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
logger.debug('GRAPHICS = \n' + pp.pformat(GRAPHICS))

# Tiles
# Tiles whose textures should be selected randomly from a list of possible textures
RANDTEXTURE = ['grass']
# Tiles that cannot be moved through
IMPASSABLE = ['water']

SOUNDS = {}

# Music
logger.debug('Loading music...')
SONGS = []
files = [f for f in os.listdir(MUSDIR) if os.path.isfile(os.path.join(MUSDIR, f))]
for filename in files:
    SONGS.append(os.path.join(MUSDIR, filename))
logger.debug('SONGS = \n' + pp.pformat(SONGS))
logger.debug('Music loaded')

logger.debug('Settings loaded successfully')
