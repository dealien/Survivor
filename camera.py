from object import Player
from settings import WINDOW_WIDTH, WINDOW_HEIGHT


class Camera(object):
    """Offsets coordinates to allow display of objects relative to the player's position."""

    def __init__(self):
        self.x_shift = self.y_shift = None

    def update(self, obj):
        """
        Center camera on input object.

        :param obj: the player or reference object

        """
        self.x_shift = 0 - obj.x
        self.y_shift = 0 - obj.y

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

    def unapply(self, obj):
        """
        :param obj:

        """
        if isinstance(obj, tuple):
            rx = obj[0] - self.x_shift - (WINDOW_WIDTH / 2)
            ry = obj[1] - self.y_shift - (WINDOW_HEIGHT / 2)
        elif isinstance(obj, (object, Player)):
            rx = obj.x - self.x_shift - (WINDOW_WIDTH / 2)
            ry = obj.y - self.y_shift - (WINDOW_HEIGHT / 2)
        else:
            raise Exception(
                f"Camera.apply() requires input to be of type tuple or Player; "
                f"got object of type {type(obj)} instead.")
        return rx, ry
