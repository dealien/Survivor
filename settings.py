import json
import os
import pprint

import pygame

import mylogger

LOGLEVEL = 3

main_log = open('main.log', 'w')
logger = mylogger.setup_custom_logger('root', LOGLEVEL)
pp = pprint.PrettyPrinter(indent=4)

logger.info('Loading settings...')

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
FONDIR = os.path.join(ADIR, 'fonts')
logger.debug(f'ROOTDIR = {ROOTDIR}')
logger.debug(f'ADIR = {ADIR}')
logger.debug(f'IMGDIR = {IMGDIR}')
logger.debug(f'AUDDIR = {AUDDIR}')
logger.debug(f'MUSICDIR = {MUSDIR}')
logger.debug(f'FONDIR = {FONDIR}')

# Config file location
CONFIGPATH = os.path.join(ROOTDIR, 'config.json')
logger.debug(f'CONFIGPATH = {CONFIGPATH}')

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
logger.info('Loading colors...')
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKWALL = (0, 0, 100)
DARKFLOOR = (50, 50, 150)
logger.info('Colors loaded.')

# Textures
logger.info('Loading graphics...')
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
logger.info('Graphics loaded.')

# Tiles
# Tiles whose textures should be selected randomly from a list of possible textures
RANDTEXTURE = ['grass']
# Tiles that cannot be moved through
IMPASSABLE = ['water']

SOUNDS = {}

# Music
logger.info('Loading music...')
SONGS = []
files = [f for f in os.listdir(MUSDIR) if os.path.isfile(os.path.join(MUSDIR, f))]
for filename in files:
    SONGS.append(os.path.join(MUSDIR, filename))
logger.debug('SONGS = \n' + pp.pformat(SONGS))
logger.info('Music loaded.')


class Settings:
    def __init__(self):
        self.LOGLEVEL = 0
        self.WINDOW_WIDTH = 0
        self.WINDOW_HEIGHT = 0
        self.debug_overlay_enabled = False
        self.load_config()

    # TODO: Use @property getter and setter for changes to WINDOW_WIDTH and WINDOW_HEIGHT

    def save_config(self):
        d = {
            'LOGLEVEL': self.LOGLEVEL,
            'WINDOW_WIDTH': self.WINDOW_WIDTH,
            'WINDOW_HEIGHT': self.WINDOW_HEIGHT
        }
        with open(CONFIGPATH, 'w') as outfile:
            json.dump(d, outfile)
        logger.debug('Settings saved to ' + CONFIGPATH)

    def load_config(self):
        try:
            with open(CONFIGPATH) as json_file:
                data = json.load(json_file)
                self.LOGLEVEL = data['LOGLEVEL']
                self.WINDOW_WIDTH = data['WINDOW_WIDTH']
                self.WINDOW_HEIGHT = data['WINDOW_HEIGHT']
            logger.warn('Settings loaded from ' + CONFIGPATH)
        except FileNotFoundError:
            # If no config file exists, load default settings
            self.LOGLEVEL = 1
            self.WINDOW_WIDTH = 900
            self.WINDOW_HEIGHT = 900
            logger.warn('No config file found. Loaded default settings.')
            self.save_config()


settings = Settings()

logger.info('Settings loaded successfully.')
