import mapgen
from logger import log


class Map():
    """The map object. Input the width, height, and smoothness. """

    def __init__(self, height, width, smoothness):
        self.height = height
        self.width = width
        self.smoothness = smoothness
        self.terrain = mapgen.generate(self.height, self.width, 4,
                                       {
                                           " ": 1,
                                           "#": 0.7,
                                           "+": 0.55,
                                           "%": 0.25
                                       })
        log.debug('Map generated (height=%d, width=%d, smoothness=%d)' % (self.height, self.width, self.smoothness))

    def __repr__(self):
        return self.terrain

    def __str__(self):
        return str(self.terrain)
