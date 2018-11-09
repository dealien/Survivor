import logging
import os

import coloredlogs
import pygame

import settings
import mapgen
from mapgen.map import Map




logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', fmt='%(asctime)s.%(msecs)03d %(name)s[%(process)d] %(levelname)s %(message)s')

new_map = Map(200, 200, 5)
mapgen.display_terrain(new_map.terrain)


class Game:
    """
    Main game object. Stores persistent information like settings, the map, etc.
    """

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT), 0, 32)
        pygame.display.set_caption('Survivor')
        # self.player = Player(os.path.join(settings.IMGDIR, 'player.bmp'), 0, 0)
        self.map = new_map
        # self.font = pygame.font.Font(os.path.join(settings.RESDIR, 'visitor1.ttf'), 18)
        # self.title_font = pygame.font.Font(os.path.join(settings.RESDIR, 'visitor1.ttf'), 36)
        self.paused = False
        self.game_over = False

        # Sounds
        self.mob_hit_player = pygame.mixer.Sound(os.path.join(settings.RESDIR, 'mobHitPlayer.wav'))
        self.add_remove_walls = pygame.mixer.Sound(os.path.join(settings.RESDIR, 'add_remove_walls.wav'))
        self.bomb = pygame.mixer.Sound(os.path.join(settings.RESDIR, 'bomb.wav'))
        self.gold = pygame.mixer.Sound(os.path.join(settings.RESDIR, 'gold.wav'))
        self.hit_wall = pygame.mixer.Sound(os.path.join(settings.RESDIR, 'hit_wall.wav'))
        self.lava = pygame.mixer.Sound(os.path.join(settings.RESDIR, 'lava.wav'))
        self.whip_breakable = pygame.mixer.Sound(os.path.join(settings.RESDIR, 'whip_breakable.wav'))
        self.whipping = pygame.mixer.Sound(os.path.join(settings.RESDIR, 'whipping.wav'))
        self.currentVolume = 1.0
        self.music_paused = False
        pygame.mixer.music.set_volume(self.currentVolume)
