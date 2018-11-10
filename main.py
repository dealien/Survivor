import os

import pygame

import mapgen
import mylogger
import settings
from mapgen.map import Map

open('main.log', 'w').close()

logger = mylogger.setup_custom_logger('root')

new_map = Map(settings.MAP_HEIGHT, settings.MAP_WIDTH, settings.MAP_SMOOTHNESS)
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
        # self.font = pygame.font.Font(os.path.join(settings.AUDDIR, 'visitor1.ttf'), 18)
        # self.title_font = pygame.font.Font(os.path.join(settings.AUDDIR, 'visitor1.ttf'), 36)
        self.paused = False
        self.game_over = False

        # Sounds
        logger.debug('Loading sounds...')
        self.sound_mob_hit_player = pygame.mixer.Sound(os.path.join(settings.AUDDIR, 'mobHitPlayer.wav'))
        self.sound_add_remove_walls = pygame.mixer.Sound(os.path.join(settings.AUDDIR, 'add_remove_walls.wav'))
        self.sound_bomb = pygame.mixer.Sound(os.path.join(settings.AUDDIR, 'bomb.wav'))
        self.sound_gold = pygame.mixer.Sound(os.path.join(settings.AUDDIR, 'gold.wav'))
        self.sound_hit_wall = pygame.mixer.Sound(os.path.join(settings.AUDDIR, 'hit_wall.wav'))
        self.sound_lava = pygame.mixer.Sound(os.path.join(settings.AUDDIR, 'lava.wav'))
        self.sound_whip_breakable = pygame.mixer.Sound(os.path.join(settings.AUDDIR, 'whip_breakable.wav'))
        self.sound_whipping = pygame.mixer.Sound(os.path.join(settings.AUDDIR, 'whipping.wav'))
        self.current_volume = 1.0
        self.music_paused = False
        pygame.mixer.music.set_volume(self.current_volume)
        logger.debug('Sounds loaded')
