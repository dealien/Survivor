import random
import sys
import time

from pygame.locals import *

from mapgen.map import Map
from settings import *
from object import *

open('main.log', 'w').close()

logger = mylogger.setup_custom_logger('root')

testrun = False
for i in sys.argv:
    if "--test-run" in i:
        testrun = True
        logger.warning("Beginning test run...")
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        logger.debug(f"SDL_VIDEODRIVER = {os.environ.get('SDL_VIDEODRIVER')}")


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
        self.font = pygame.font.Font(os.path.join(ADIR, 'Sarabun-Regular.ttf'), 18)
        self.small_font = pygame.font.Font(os.path.join(ADIR, 'RobotoMono-Bold.ttf'), 12)
        self.title_font = pygame.font.Font(os.path.join(ADIR, 'PT_Sans-Web-Regular.ttf'), 36)
        self.paused = False
        self.running = True

        # Sounds
        self.current_volume = 0.25
        self.music_paused = False
        self.current_song = None
        self.play_next_song()

    @property
    def current_volume(self):
        return self._current_volume

    @current_volume.getter
    def current_volume(self):
        if not self._current_volume == pygame.mixer.music.get_volume():
            self._current_volume = pygame.mixer.music.get_volume()
        return self._current_volume

    @current_volume.setter
    def current_volume(self, val):
        self._current_volume = val
        pygame.mixer.music.set_volume(self._current_volume)

    def play_sound(self, path):
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
        next_song = random.choice(SONGS)
        while next_song == self.current_song:
            next_song = random.choice(SONGS)
        self.current_song = next_song
        pygame.mixer.music.load(next_song)
        pygame.mixer.music.play()
        logger.debug('Now playing ' + os.path.split(self.current_song)[1])


class Camera(object):
    """Offsets coordinates to allow display of objects relative to the player's position."""

    def __init__(self):
        self.x_shift = self.y_shift = None

    def update(self):
        """ """
        self.x_shift = 0 - game.player.x
        self.y_shift = 0 - game.player.y

    def apply(self, obj):
        """
        :param obj: 

        """
        if isinstance(obj, tuple):
            rx = obj[0] + self.x_shift + (WINDOW_WIDTH / 2)
            ry = obj[1] + self.y_shift + (WINDOW_HEIGHT / 2)
        elif isinstance(obj, (object, Player)):
            rx = obj.x + self.x_shift + (WINDOW_WIDTH / 2)
            ry = obj.y + self.y_shift + (WINDOW_HEIGHT / 2)
        else:
            raise Exception(
                f"Camera.apply() requires input to be of type tuple or Player(); "
                f"got object of type {type(obj)} instead.")
        return rx, ry


def draw_debug_overlay():
    mouse_pos = pygame.mouse.get_pos()
    text = game.small_font.render('[' + str(mouse_pos[0]) + ', ' + str(mouse_pos[1]) + ']', True, (255, 255, 255))
    r = text.get_rect()
    w, h = pygame.display.get_surface().get_size()
    x = w - text.get_width()
    r[0] = x
    pygame.draw.rect(game.surface, (0, 0, 0), r)
    game.surface.blit(text, (x, 0))


def render_all(game):
    """
    Updates the display output, drawing all tiles, objects, and the player.

    :param game: the main game object

    """
    # render_start = time.perf_counter()
    game.camera.update()
    game.surface.fill((0, 0, 0))
    for a in range(len(game.map.tilemap)):
        for b in range(len(game.map.tilemap[a])):
            # Set the x and y coordinates based on the number of pixels per tile image
            y = a * IMGSIZE
            x = b * IMGSIZE
            # Draw from the perspective of the camera
            game.surface.blit(game.map.tilemap[a][b].texture, game.camera.apply((x, y)))
    game.surface.blit(game.player.image, game.camera.apply(game.player))  # Draw the player
    if debug_overlay_enabled:
        draw_debug_overlay()
    pygame.display.update()
    # render_end = time.perf_counter()
    # logger.debug(f'Rendered in {render_end - render_start} seconds')


pygame.init()
game = Game()
SONG_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(SONG_END)

# When the script is run using the "--test-run" argument, test actions used in the main loop, then exit.
if testrun:
    game.player.move(270, game)
    game.player.move(90, game)
    game.player.move(0, game)
    game.player.move(180, game)
    # Exit after testing before the main loop
    sys.exit()

debug_overlay_enabled = False

# Main game loop. Detect keyboard input for character movements, etc.
# Controls:
# - Escape to quit
# - WASD, arrow keys, or numpad 2468 to move
#   - Hold shift while pressing a movement key to turn in place
# - E, Z, or numpad 5 to interact
# - Backslash to toggle debug overlay
while game.running:
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            game.running = False
        if event.type == KEYDOWN:

            # Quit the game when escape is pressed
            if event.key == K_ESCAPE:
                game.running = False

            # Move player normally
            if pygame.key.get_mods() & KMOD_SHIFT and (event.key == K_LEFT or event.key == K_a or event.key == K_KP4):
                game.player.turnto(90, False)
            if pygame.key.get_mods() & KMOD_SHIFT and (event.key == K_RIGHT or event.key == K_d or event.key == K_KP6):
                game.player.turnto(270, False)
            if pygame.key.get_mods() & KMOD_SHIFT and (event.key == K_UP or event.key == K_w or event.key == K_KP8):
                game.player.turnto(0, False)
            if pygame.key.get_mods() & KMOD_SHIFT and (event.key == K_DOWN or event.key == K_s or event.key == K_KP2):
                game.player.turnto(180, False)

            # Turn the player in place
            if (event.key == K_LEFT or event.key == K_a or event.key == K_KP4) \
                    and not pygame.key.get_mods() & KMOD_SHIFT:
                game.player.move(90, game)
            if (event.key == K_RIGHT or event.key == K_d or event.key == K_KP6) \
                    and not pygame.key.get_mods() & KMOD_SHIFT:
                game.player.move(270, game)
            if (event.key == K_UP or event.key == K_w or event.key == K_KP8) \
                    and not pygame.key.get_mods() & KMOD_SHIFT:
                game.player.move(0, game)
            if (event.key == K_DOWN or event.key == K_s or event.key == K_KP2) \
                    and not pygame.key.get_mods() & KMOD_SHIFT:
                game.player.move(180, game)

            # Interact with the tile in front of the player
            if event.key == K_z or event.key == K_e or event.key == K_KP5:
                game.player.interact(game)

            # Toggle debug overlay
            if event.key == K_BACKSLASH:
                debug_overlay_enabled = not debug_overlay_enabled
        if event.type == SONG_END:
            game.play_next_song()
    render_all(game)
    game.clock.tick(50)
pygame.quit()
