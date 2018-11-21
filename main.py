from pygame.locals import *

from mapgen.map import Map
from settings import *
from object import *

open('main.log', 'w').close()

logger = mylogger.setup_custom_logger('root')


class Game:
    """
    Main game object. Stores persistent information like settings, the map, etc.
    """

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
        pygame.display.set_caption('Survivor')  # Set window title
        self.player = Player(textures['player'], (MAP_WIDTH / 2) * IMGSIZE, (MAP_HEIGHT / 2) * IMGSIZE)
        new_map = Map(MAP_HEIGHT, MAP_WIDTH, MAP_SMOOTHNESS)
        self.map = new_map
        self.camera = Camera()
        # self.font = pygame.font.Font(os.path.join(AUDDIR, 'visitor1.ttf'), 18)
        # self.title_font = pygame.font.Font(os.path.join(AUDDIR, 'visitor1.ttf'), 36)
        self.paused = False
        self.game_over = False

        # Sounds
        # TODO: Make all sounds live in a main "sound" object
        self.sound_mob_hit_player = pygame.mixer.Sound(os.path.join(AUDDIR, 'mobHitPlayer.wav'))
        self.sound_gold = pygame.mixer.Sound(os.path.join(AUDDIR, 'gold.wav'))
        self.sound_hit_wall = pygame.mixer.Sound(os.path.join(AUDDIR, 'hit_wall.wav'))
        self.current_volume = 1.0
        self.music_paused = False
        pygame.mixer.music.set_volume(self.current_volume)


class Camera(object):  # Offsets coordinates to allow display of objects relative to player position
    def __init__(self):
        self.x_shift = self.y_shift = None

    def update(self):
        self.x_shift = 0 - game.player.x
        self.y_shift = 0 - game.player.y

    def apply(self, obj):
        if type(obj) is tuple:
            rx = obj[0] + self.x_shift + (WINDOW_WIDTH / 2)
            ry = obj[1] + self.y_shift + (WINDOW_HEIGHT / 2)
        elif type(obj) is object or Player:
            rx = obj.x + self.x_shift + (WINDOW_WIDTH / 2)
            ry = obj.y + self.y_shift + (WINDOW_HEIGHT / 2)
        return rx, ry


def render_all(game):
    game.camera.update()
    game.surface.fill((0, 0, 0))
    for a in range(len(game.map.tilemap)):
        for b in range(len(game.map.tilemap[a])):
            # Set the x and y coordinates by the number of pixels the image is, 16 , 32 etc.
            y = a * IMGSIZE
            x = b * IMGSIZE
            # Draw from the perspective of the camera
            game.surface.blit(game.map.tilemap[a][b].texture, game.camera.apply((x, y)))
    game.surface.blit(textures['player'], game.camera.apply(game.player))  # Draw the player
    pygame.display.update()


pygame.init()
game = Game()
while not game.game_over:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_LEFT or event.key == K_KP4:
                game.player.move(270, game)
            if event.key == K_RIGHT or event.key == K_KP6:
                game.player.move(90, game)
            if event.key == K_UP or event.key == K_KP8:
                game.player.move(0, game)
            if event.key == K_DOWN or event.key == K_KP2:
                game.player.move(180, game)

    render_all(game)
    game.clock.tick(50)
