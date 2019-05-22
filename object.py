import random

import pygame

from settings import *
from settings import RANDTEXTURE, GRAPHICS, IMPASSABLE, IMGSIZE


class Object(pygame.sprite.Sprite):
    """ """

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
        """
        :param surface: 

        """
        image = pygame.transform.rotate(self.base_image, self.dir)
        rect = image.get_rect()
        surface.blit(image, rect)


class Player(Object):
    """ """

    def __init__(self, image, x, y):
        Object.__init__(self, image, x, y)
        self.weapon = None
        self.image = self.base_image

    @property
    def x(self):
        """ """
        return self.rect[0]

    @x.setter
    def x(self, val):
        """
        :param val: 

        """
        self.rect[0] = val

    @property
    def y(self):
        """ """
        return self.rect[1]

    @y.setter
    def y(self, val):
        """
        :param val: 

        """
        self.rect[1] = val

    def move(self, d, game):
        """
        :param d: param game:
        :param game: 

        """
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
        if self.rect is new_position:
            debug_text = (
                f'Player moved from ({old_position[0]}, {old_position[1]}) to ({new_position[0]}, {new_position[1]})')
        else:
            debug_text = (
                f'Movement blocked from ({old_position[0]}, {old_position[1]})'
                f' to ({new_position[0]}, {new_position[1]})')
        logger.debug(f'{debug_text}, now facing {str(self.dir)} ({repr(self.dir)})')

    def turnto(self, d, moved=True):
        """
        Turns the player to face the specified direction.

        :type d: int
        :param d: The direction to face. Must be 0, 90, 180, or 270.
        :param moved: If the player was just moved, the direction change log output will be suppressed in favor of the
        one output by ``player.move()``. (Default value = True)

        """
        self.dir = Direction(d)
        self.image = pygame.transform.rotate(self.base_image, d)
        if not moved:
            logger.debug(f'Player turned to face {str(self.dir)} ({repr(self.dir)})')

    def check_collision(self, game, old_position, new_position):
        """
        Ensures that a given movement is possible and that nothing is in the way. Movement can be blocked by map
        borders, objects, or impassable tiles. Some tiles may be impassable without certain equipment.

        :param game: The main game object
        :param old_position: The starting position
        :param new_position: The target position
        :returns: If the movement is blocked, returns the starting position. Otherwise, returns the target position.

        """
        newx = int(new_position[0] / game.player.rect[2])
        newy = int(new_position[1] / game.player.rect[3])
        if -1 < new_position[0] < game.player.rect[3] * game.map.width \
                and -1 < new_position[1] < game.player.rect[3] * game.map.height:
            target = game.map.tilemap[newy][newx]
            if not target.collisions and target.passable:
                position = new_position
            else:
                game.play_sound('hit_wall.wav')
                position = old_position
        else:
            game.play_sound('hit_wall.wav')
            position = old_position
        return position

    def interact(self, game):
        """
        Allows the player to interact with the environment.

        :param game: The main game object

        """
        map_x = int(self.x / IMGSIZE)
        map_y = int(self.y / IMGSIZE)
        target_x = self.x
        target_y = self.y
        if str(self.dir) is NORTH:
            map_y -= 1
            target_y = self.y - IMGSIZE
        elif str(self.dir) is WEST:
            map_x -= 1
            target_x = self.x - IMGSIZE
        elif str(self.dir) is SOUTH:
            map_y += 1
            target_y = self.y - IMGSIZE
        elif str(self.dir) is EAST:
            map_x += 1
            target_x = self.x - IMGSIZE
        target: Tile = game.map.tilemap[map_y][map_x]
        logger.debug(f"Interaction target at ({target_x}, {target_y}) is {target.material}")
        return True


class Direction():
    """ """

    def __init__(self, d=0):
        self.direction = d

    def __repr__(self):
        return repr(self.direction)  # Allows representation as int type

    def __str__(self):
        directions = {'0': 'NORTH',  # North
                      '90': 'WEST',  # West
                      '180': 'SOUTH',  # South
                      '270': 'EAST'}  # East
        d = self.direction
        return directions[str(d)]


class Tile:
    """
    Holds information about a specific tile on the map.
    """

    def __init__(self, material, x, y):
        """
        :param material: The name of the material
        :param x: The x position on the map
        :param y: The y position on the map
        """
        self.material = material
        # Rotate the texture if necessary
        if material in RANDTEXTURE:
            images = []
            for i in GRAPHICS:
                if material in i:
                    images.append(GRAPHICS[i])
            image = random.choice(images)
            self.rot = random.randint(0, 3) * 90
            self.texture = pygame.transform.rotate(image, self.rot)
        else:
            image = GRAPHICS[material]
            self.rot = 0
            self.texture = image
        self.collisions = False
        self.passable = self.material not in IMPASSABLE
        self.durability = -1
        self.rect = pygame.Rect(x, y, IMGSIZE, IMGSIZE)

    def __str__(self):
        return f'{self.material} tile at [{self.rect[0]}, {self.rect[1]}]'
