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
    """Main game object. Stores persistent information like settings, the map, the player, etc."""

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

        # Sounds
        self.current_volume = 0.05
        self.music_paused = False
        self.current_song = None
        self.play_next_song()

    @property
    def current_volume(self):
        return self._current_volume

    @current_volume.getter
    def current_volume(self):
        if not pygame.mixer.get_init() is None:
            if not self._current_volume == pygame.mixer.music.get_volume():
                self._current_volume = pygame.mixer.music.get_volume()
        return self._current_volume

    @current_volume.setter
    def current_volume(self, val):
        self._current_volume = val
        if not pygame.mixer.get_init() is None:
            pygame.mixer.music.set_volume(self._current_volume)

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
    w, h = pygame.display.get_surface().get_size()
    mouse_from_center = window_to_screen_pos(mouse_pos)

    text_mouse_pos = game.small_font.render(
        f'Mouse: [{mouse_pos[0]}, {mouse_pos[1]}], [{mouse_from_center[0]}, {mouse_from_center[1]}]', True,
        (255, 255, 255))
    text_mouse_pos_rect = text_mouse_pos.get_rect()
    text_mouse_pos_x = w - text_mouse_pos.get_width()
    text_mouse_pos_rect[0] = text_mouse_pos_x

    text_player_pos = game.small_font.render(f'Player: [{game.player.rect[0]}, {game.player.rect[1]}] '
                                             f'({int(game.player.rect[0] / 16)}, {int(game.player.rect[1] / 16)}); '
                                             f'facing {str(game.player.dir)} ({repr(game.player.dir)})', True, (255, 255, 255))
    text_player_pos_rect = text_player_pos.get_rect()
    text_player_pos_x = w - text_player_pos.get_width()
    text_player_pos_rect[0] = text_player_pos_x
    text_player_pos_rect[1] = 17

    # text_obj_at_mouse_pos = game.small_font.render(f'Object: [{game.player.rect[0]}, {game.player.rect[1]}] '
    #                                          f'({int(game.player.rect[0] / 16)}, {int(game.player.rect[1] / 16)}); '
    #                                          f'facing {str(game.player.dir)} ({repr(game.player.dir)})'
    #                                          , True, (255, 255, 255))
    # text_obj_at_mouse_pos_rect = text_obj_at_mouse_pos.get_rect()
    # text_obj_at_mouse_pos_x = w - text_obj_at_mouse_pos.get_width()
    # text_obj_at_mouse_pos_rect[0] = text_obj_at_mouse_pos_x
    # text_obj_at_mouse_pos_rect[1] = 17

    pygame.draw.rect(game.surface, (0, 0, 0), text_mouse_pos_rect)
    game.surface.blit(text_mouse_pos, text_mouse_pos_rect)
    pygame.draw.rect(game.surface, (0, 0, 0), text_player_pos_rect)
    game.surface.blit(text_player_pos, text_player_pos_rect)
    # pygame.draw.rect(game.surface, (0, 0, 0), text_obj_at_mouse_pos)
    # game.surface.blit(text_player_pos, text_obj_at_mouse_pos)


def get_debug_info_at_pos(game, pos):
    # TODO: Add this information to the debug overlay
    mx, my = game.camera.unapply(pos)
    mx = mx / 16
    my = my / 16
    imx = int(mx)
    imy = int(my)
    selected_tile = None
    try:
        selected_tile = game.map.tilemap[imy][imx]
        logger.debug(selected_tile)
    except IndexError:
        logger.warning(f'Coordinates out of range: [{imx}, {imy}]')
    return selected_tile, mx, my
