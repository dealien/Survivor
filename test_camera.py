from unittest import TestCase

from camera import Camera
from object import Player
from settings import GRAPHICS, MAP_WIDTH, IMGSIZE, MAP_HEIGHT


class TestCamera(TestCase):
    @classmethod
    def setUpClass(cls):
        global player, camera, x_shift, y_shift, tile_pos, rendered_pos, mouse_pos
        player = Player(GRAPHICS['player'], (MAP_WIDTH / 2) * IMGSIZE, (MAP_HEIGHT / 2) * IMGSIZE)
        camera = Camera()
        camera.update(player)
        x_shift = -400
        y_shift = -400
        tile_pos = (15, 27)
        rendered_pos = (143.0, -65.0)
        mouse_pos = (520, 297)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_apply(self):
        assert camera.apply(tile_pos) == rendered_pos

    def test_unapply(self):
        assert camera.unapply(camera.apply(tile_pos)) == tile_pos
        assert camera.unapply(rendered_pos) == tile_pos
