import os
import random
from math import floor

import pygame

from camera import Camera
from mapgen.map import Map
from object import Player
from settings import *
from settings import logger


class Game:
    """Main game object. Stores persistent information such as the map, the player, etc."""

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
        pygame.display.set_caption('Survivor')  # Set window title
        self.player = Player(GRAPHICS['player'], (MAP_WIDTH / 2) * IMGSIZE, (MAP_HEIGHT / 2) * IMGSIZE)
        new_map = Map(MAP_HEIGHT, MAP_WIDTH, MAP_SMOOTHNESS)
        self.map = new_map
        self.camera = Camera()
        self.font = pygame.font.Font(os.path.join(FONDIR, 'Sarabun-Regular.ttf'), 18)
        self.small_font = pygame.font.Font(os.path.join(FONDIR, 'RobotoMono-Bold.ttf'), 12)
        self.title_font = pygame.font.Font(os.path.join(FONDIR, 'PT_Sans-Web-Regular.ttf'), 36)
        self.paused = False
        self.running = True

        self.current_volume = settings.current_volume
        self.current_song = None
        self.play_next_song()

    @property
    def current_volume(self):
        if not pygame.mixer.get_init() is None:
            settings.current_volume = pygame.mixer.music.get_volume()
            return pygame.mixer.music.get_volume()
        else:
            return 0

    @current_volume.setter
    def current_volume(self, val):
        if not pygame.mixer.get_init() is None:
            pygame.mixer.music.set_volume(val)
            settings.current_volume = val

    def play_sound(self, path):
        if not pygame.mixer.get_init() is None:
            if not ('\\' in path and not ('/' in path)):
                path = os.path.join(AUDDIR, path)
            sound = SOUNDS.get(path)
            if sound is None:
                canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
                sound = pygame.mixer.Sound(canonicalized_path)
                SOUNDS[path] = sound
            sound.set_volume(self.current_volume)
            sound.play()

    def play_next_song(self):
        if not pygame.mixer.get_init() is None:
            next_song = random.choice(SONGS)
            while next_song == self.current_song:
                next_song = random.choice(SONGS)
            self.current_song = next_song
            pygame.mixer.music.load(next_song)
            pygame.mixer.music.play()
            logger.debug('Now playing ' + os.path.split(self.current_song)[1])


def round_down(num, divisor):
    return floor(num / divisor) * divisor


def window_to_screen_pos(pos):
    return pos[0] - (WINDOW_WIDTH / 2), -(pos[1] - (WINDOW_HEIGHT / 2))


def screen_to_window_pos(pos):
    return pos[0] + (WINDOW_WIDTH / 2), (WINDOW_HEIGHT / 2) - pos[1]


def draw_debug_overlay(game):
    mouse_pos = pygame.mouse.get_pos()
    mouse_from_center = window_to_screen_pos(mouse_pos)
    i = get_debug_info_at_pos(game, pygame.mouse.get_pos())
    tile_info = str(i[0])

    debug_lines = []
    debug_lines.append(f'Mouse: [{mouse_pos[0]}, {mouse_pos[1]}], [{mouse_from_center[0]}, {mouse_from_center[1]}]')
    debug_lines.append(tile_info)
    debug_lines.append(f'Player: [{game.player.rect[0]}, {game.player.rect[1]}] '
                       f'({int(game.player.rect[0] / 16)}, {int(game.player.rect[1] / 16)}); '
                       f'facing {str(game.player.dir)} ({repr(game.player.dir)})')
    debug_lines.append(f'Object: [{game.player.rect[0]}, {game.player.rect[1]}] '
                       f'({int(game.player.rect[0] / 16)}, {int(game.player.rect[1] / 16)}); '
                       f'facing {str(game.player.dir)} ({repr(game.player.dir)})')

    voffset = 0
    w, h = pygame.display.get_surface().get_size()

    for line in debug_lines:
        debug_line = game.small_font.render(line, True, (255, 255, 255))
        debug_line_rect = debug_line.get_rect()
        debug_line_x = w - debug_line.get_width()
        debug_line_rect[0] = debug_line_x
        debug_line_rect[1] = voffset

        pygame.draw.rect(game.surface, (0, 0, 0), debug_line_rect)
        game.surface.blit(debug_line, debug_line_rect)

        voffset += 17


def get_debug_info_at_pos(game, pos):
    mx, my = game.camera.unapply(pos)
    mx = mx / 16
    my = my / 16
    imx = int(mx)
    imy = int(my)
    selected_tile = None
    try:
        selected_tile = game.map.tilemap[imy][imx]
    except IndexError:
        pass
    return selected_tile, mx, my
