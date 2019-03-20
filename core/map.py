from typing import List

import numpy


class Beacon:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, x, y):
        numpy.linalg.norm(numpy.array([self.x, self.y]) - numpy.array([x, y]))


class Map:

    def __init__(self):
        self.beacons = []

    def add_beacons(self, beacons: List[Beacon]):
        self.beacons.extend(beacons)
