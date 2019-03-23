from typing import List

import numpy


class Beacon:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def distance_to(self, x, y) -> float:
        return numpy.linalg.norm(numpy.array([self.x, self.y]) - numpy.array([x, y]))


class Map:

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.start_x = 0.5 * self.width
        self.start_y = 0.5 * self.height

        self.beacons = []

    def add_beacon(self, beacon: Beacon):
        self.beacons.append(beacon)

    def add_beacons(self, beacons: List[Beacon]):
        self.beacons.extend(beacons)

    def get_beacon_distances(self, x, y):
        return [beacon.distance_to(x, y) for beacon in self.beacons]
