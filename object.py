import random

from settings import *


class Object(pygame.sprite.Sprite):
    # this is a generic object: player, monster, chest, stairs etc.
    def __init__(self, image, x, y, kind=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.image.set_colorkey(self.image.get_at((0, 0)))  # makes the border color transparent no matter what!
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.kind = kind

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Player(Object):
    def __init__(self, image, x, y):
        Object.__init__(self, image, x, y)
        self.weapon = None

    @property
    def x(self):
        return self.rect[0]

    @x.setter
    def x(self, val):
        self.rect[0] = val

    @property
    def y(self):
        return self.rect[1]

    @y.setter
    def y(self, val):
        self.rect[1] = val

    def move(self, dx, dy, game):
        new_position = self.rect.move(dx, dy)
        old_position = self.rect
        self.rect = self.check_collision(game, old_position, new_position)

    def check_collision(self, game, old_position, new_position):
        # If something blocks the movement, the position returns unchanged, otherwise it returns the new position
        if game.map.tilemap[int(new_position[0] / game.player.rect[2])][
            int(new_position[1] / game.player.rect[3])].collisions is False and \
                -1 < new_position[0] < game.player.rect[3] * game.map.width and \
                -1 < new_position[1] < game.player.rect[3] * game.map.height:
            logger.debug(f'Player moved from {old_position} to {new_position}')
            position = new_position
        else:
            game.sound_hit_wall.play()
            logger.debug(f'Movement blocked from {old_position} to {new_position}')
            position = old_position
        return position
