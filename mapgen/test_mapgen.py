from unittest import TestCase

import mapgen


class TestMapgen(TestCase):

    def test_generate_terrain(self):
        map = mapgen.generate_terrain(50, 50, 4,
                                      {
                                          '*': 0.4,
                                          " ": 1,
                                          "+": 0.75,
                                          "#": 0.45
                                      })
        assert len(map) == 50
        assert len(map[0]) == 50
