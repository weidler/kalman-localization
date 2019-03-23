import math
from typing import List

import numpy


class Beacon:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def distance_to(self, x, y) -> float:
        return numpy.linalg.norm(numpy.array([self.x, self.y]) - numpy.array([x, y]))

    def bearing(self, x, y, heading):
        endpoint_heading = (math.cos(heading), math.sin(heading))
        vector_heading = numpy.array((x - endpoint_heading[0], y - endpoint_heading[1]))
        vector_bearing = numpy.array((x - self.x, y - self.y))

        bearing = numpy.arccos(numpy.dot(vector_bearing, vector_heading)/(numpy.linalg.norm(vector_heading) * numpy.linalg.norm(vector_heading)))
        return bearing


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

    def get_bearings(self, x, y, heading):
        return [beacon.bearing(x, y, heading) for beacon in self.beacons]

    def get_beacons_in_distance(self, x, y, dist):
        return [beacon for beacon in self.beacons if beacon.distance_to(x, y) <= dist]