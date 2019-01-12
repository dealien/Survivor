from settings import *


class Object(pygame.sprite.Sprite):
    # This is a generic object: player, monster, chest, stairs etc.
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.base_image = image
        # Make the border color transparent no matter what!
        self.base_image.set_colorkey(self.base_image.get_at((0, 0)))
        self.image = self.base_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.dir = Direction(0)

    def draw(self, surface):
        image = pygame.transform.rotate(self.base_image, self.dir)
        rect = image.get_rect()
        surface.blit(image, rect)


class Player(Object):
    def __init__(self, image, x, y):
        Object.__init__(self, image, x, y)
        self.weapon = None
        self.image = self.base_image

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

    def move(self, d, game):
        dirs = {
            '0': (0, -IMGSIZE),  # North
            '90': (-IMGSIZE, 0),  # West
            '180': (0, IMGSIZE),  # South
            '270': (IMGSIZE, 0)  # East
        }
        dx, dy = dirs[str(d)]
        new_position = self.rect.move(dx, dy)
        old_position = self.rect
        self.turnto(d)
        self.image = pygame.transform.rotate(self.base_image, d)
        self.rect = self.check_collision(game, old_position, new_position)

    def turnto(self, d):
        self.dir = Direction(d)

    def check_collision(self, game, old_position, new_position):
        # If something blocks the movement, the position returns unchanged, otherwise it returns the new position
        if game.map.tilemap[int(new_position[0] / game.player.rect[2])][
            int(new_position[1] / game.player.rect[3])].collisions is False and \
                -1 < new_position[0] < game.player.rect[3] * game.map.width and \
                -1 < new_position[1] < game.player.rect[3] * game.map.height:
            logger.debug(
                f'Player moved from ({old_position[0]}, {old_position[1]}) to ({new_position[0]}, {new_position[1]})')
            position = new_position
        else:
            game.sound_hit_wall.play()
            logger.debug(
                f'Movement blocked from ({old_position[0]}, {old_position[1]})'
                f' to ({new_position[0]}, {new_position[1]})')
            position = old_position
        logger.debug(f'Player is now facing {str(self.dir)} ({repr(self.dir)})')
        return position


class Direction():
    def __init__(self, d=0):
        self.direction = d

    def __repr__(self):
        return repr(self.direction)  # Allows representation as int type

    def __str__(self):
        directions = {'0': 'NORTH',  # North
                      '90': 'EAST',  # East
                      '180': 'SOUTH',  # South
                      '270': 'WEST'}  # West
        d = self.direction
        return directions[str(d)]
