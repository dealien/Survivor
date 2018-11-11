import random

from settings import *


class Object(pygame.sprite.Sprite):
    # this is a generic object: player, monster, chest, stairs etc.
    def __init__(self, image, x, y, kind=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert()
        self.image.set_colorkey(self.image.get_at((0, 0)))  # makes the border color transparent no matter what!
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.kind = kind

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Player(Object):
    def __init__(self):
        self.weapon = None

    def move(self, dx, dy, game):
        new_position = self.rect.move(dx, dy)
        old_position = self.rect
        self.rect = self.check_collision(game, old_position, new_position)

    def check_collision(self, game, old_position, new_position):
        # TODO: create check_collision()
        # If something blocks the movement, the position returns unchanged, otherwise it returns the new position
        if game.map.tilemap[new_position[0]][new_position[1]].collisions is True:
            position = new_position
        else:
            game.hit_wall.play()
            position = old_position
        return position
