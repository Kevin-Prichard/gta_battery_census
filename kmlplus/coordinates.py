from geographiclib.geodesic import Geodesic
from geopy import distance as gp


class Coordinate:
    def __init__(self, point: tuple[float, float] = (-1, -1),
                 name=None, height=None):
        self.name = name
        self.height = height
        self._latitude: float = point[1]
        self._longitude: float = point[0]

    @property
    def latitude(self) -> float:
        return self._latitude

    @latitude.setter
    def latitude(self, a_latitude: float):
        self._latitude = a_latitude

    @property
    def longitude(self) -> float:
        return self._longitude

    @longitude.setter
    def longitude(self, a_longitude: float):
        self._longitude = a_longitude

    @property
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, a_height: float):
        self._height = a_height

    """Takes argument of self and returns a string representation of the coordinates and height"""
    def __str__(self):
        the_string = "{}, {}, {}".format(self.latitude, self.longitude, self.height)
        return the_string

    """
    Takes zero arguments and returns a .kml readable tuple in the xyz format.
    """
    #  Gives an xyz tuple which is readable by kml
    def kml_tuple(self):
        return self.longitude, self.latitude, self.height
