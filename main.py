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
        pygame.display.set_caption('Survivor')
        self.player = Player(textures['player'], 0, 0)
        new_map = Map(MAP_HEIGHT, MAP_WIDTH, MAP_SMOOTHNESS)
        self.map = new_map
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


class Camera(object):
    def __init__(self, width, height):
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def render_all(game):
    game.surface.fill((0, 0, 0))
    for a in range(len(game.map.tilemap)):
        for b in range(len(game.map.tilemap[a])):
            y = a * IMGSIZE  # This sets the x and y coordinates by the number of pixels the image is, 16 , 32 etc.
            x = b * IMGSIZE
            game.surface.blit(game.map.tilemap[a][b].texture, (x, y))
    game.player.draw(game.surface)
    pygame.display.update()


pygame.init()
game = Game()
camera = Camera(WINDOW_WIDTH, WINDOW_HEIGHT)
while not game.game_over:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_LEFT or event.key == K_KP4:
                game.player.move(-IMGSIZE, 0, game)
            if event.key == K_RIGHT or event.key == K_KP6:
                game.player.move(IMGSIZE, 0, game)
            if event.key == K_UP or event.key == K_KP8:
                game.player.move(0, -IMGSIZE, game)
            if event.key == K_DOWN or event.key == K_KP2:
                game.player.move(0, IMGSIZE, game)

    render_all(game)
    game.clock.tick(50)
