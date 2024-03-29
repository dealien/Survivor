import sys
import time

from pygame.locals import *

from game import Game, draw_debug_overlay, get_debug_info_at_pos
from settings import *
from settings import logger

# TODO: Include the test run in a proper test
testrun = False
for i in sys.argv:
    if "--test-run" in i:
        testrun = True
        logger.warning("Beginning test run...")
        logger.debug(f"SDL_VIDEODRIVER = {os.environ.get('SDL_VIDEODRIVER')}")


def render_all():
    """
    Updates the display output, drawing all tiles, objects, and the player.
    """
    render_start = time.perf_counter()
    game.camera.update(game.player)
    game.surface.fill((0, 0, 0))
    for a in range(len(game.map.tilemap)):
        for b in range(len(game.map.tilemap[a])):
            # Set the x and y coordinates based on the number of pixels per tile image
            y = a * IMGSIZE
            x = b * IMGSIZE
            # Draw tile from the perspective of the camera
            game.surface.blit(game.map.tilemap[a][b].texture, game.camera.apply((x, y)))
            if game.map.objectmap[a][b] is not None:
                # Draw object from the perspective of the camera
                game.surface.blit(game.map.objectmap[a][b].image, game.camera.apply((x, y)))
    game.surface.blit(game.player.image, game.camera.apply(game.player))  # Draw the player
    if settings.debug_overlay_enabled:
        draw_debug_overlay(game)
    pygame.display.update()
    render_end = time.perf_counter()
    # logger.debug(f'Rendered in {render_end - render_start} seconds')
    if testrun:
        render_times.append(render_end - render_start)


pygame.init()
if pygame.mixer.get_init() is None:
    logger.warning('No available audio device. Audio output disabled.')
game = Game()
SONG_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(SONG_END)

# When the script is run using the "--test-run" argument, test actions used in the main loop, then exit.
timeout = 0
render_times = []
if testrun:
    timeout = time.time() + 10

# Main game loop. Detect keyboard input for character movements, etc.
# Controls:
# - Escape to quit
# - WASD, arrow keys, or numpad 2468 to move
#   - Hold shift while pressing a movement key to turn in place
# - E, Z, or numpad 5 to interact
# - Backslash to toggle debug overlay
# - M to toggle mute

while game.running:
    if testrun and time.time() > timeout:
        t = sum(render_times) / len(render_times)
        print('Average time to render frames: ' + str(t))
        break
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
                settings.debug_overlay_enabled = not settings.debug_overlay_enabled
                logger.debug('Debug overlay ' + 'enabled' if settings.debug_overlay_enabled else 'disabled')

            if event.key == K_m:
                if not settings.music_muted:
                    pygame.mixer.music.set_volume(0)
                else:
                    pygame.mixer.music.set_volume(settings.current_volume)
                settings.music_muted = not settings.music_muted
                logger.debug('Music ' + 'muted' if settings.music_muted else 'unmuted')

        # When the current song ends, play the next one
        if event.type == SONG_END:
            logger.debug('Song ended')
            game.play_next_song()

    render_all()
    game.clock.tick(50)

logger.info('Quitting game...')
pygame.quit()
