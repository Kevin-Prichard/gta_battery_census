import copy

from typing import List

from kmlplus.coordinates import Coordinate

"""
This function will create lower and upper layers as well as the sides.  It is limited to 'flat' layers ie each layer
must be the same height.  It offers a quick way to create a polygon.  Accepts args and kwargs of lower_height,
upper_height, origin and sort.  Returns two LinePaths for the lower and upper layers and a list of lists containing 
tuples for the sides.  
"""


def quick_polygon(points, lower_height: float = 0, upper_height: float = 0, origin=None, sort=False):
    origin = origin
    sort = sort

    lower_layer = LinePath(points, height=lower_height, sort=sort, origin=origin)
    upper_layer, sides = lower_layer.create_layer_and_sides(height=upper_height)

    return lower_layer, upper_layer, sides


"""
LinePath is used to create polygons by combining Coordinate objects.  LinePath objects connect coordinate objects via
straight lines when used in conjunction with polygon classes such as the 'floatingpolygon' class.  If a circle or 'arc'
is required, you can first use the ArcPath class and provide it as a * argument to the LinePath class.

If the Coordinate instances provided are not yet in decimal format, the LinePath class will convert it to decimal
automatically.
"""


class LinePath:
    def __init__(self, points: List[tuple[float, float]], height=None, sort=False, origin=None):
        self.sort = sort
        self.height = height
        self.origin = origin

        self.points = self.generate_coordinate_object(points)

        # If user has entered a height, check it is a valid float or int
        if self.height is not None:

            # If user passes a height value, change altitude values for all coordinate instances passed as arguments
            for coord in self.points:
                coord.height = self.height

        self.kml_coordinate_list = self.kml_format()

    def __getitem__(self, index):
        return self.kml_coordinate_list[index]

    def __str__(self):
        return "LinePath instance containing {} kml readable Coordinate instances - {}".format(
            len(self.kml_coordinate_list), [str(x) for x in self.kml_coordinate_list])

    def __len__(self):
        return len(self.points)

    @staticmethod
    def validate_int(a_value):
        if not isinstance(a_value, int):
            try:
                a_value = int(a_value)
                return a_value
            except ValueError as error:
                print(error)
                print('Defaulting value to int 50')
                return 50
        else:
            return a_value

    @staticmethod
    def sides_depreciated():
        deprecated_warning = "LinePath.sides deprecated since v2.0.  Please use LinePath.create_layer_and_sides()" \
                             " to return a new LinePath layer and sides.  Alternatively call .create_sides() to return" \
                             " a list of sides between this linepath and another."
        return deprecated_warning

    def generate_coordinate_object(self, points) -> List[Coordinate]:
        list_to_return = []
        for point in points:
            if not isinstance(point, Coordinate):
                try:
                    if self.height is not None:
                        new_coordinate = Coordinate(point, height=self.height)
                    else:
                        new_coordinate = Coordinate(point)
                    list_to_return.append(new_coordinate)
                except TypeError as error:
                    print(error)
            elif isinstance(point, Coordinate):
                list_to_return.append(point)
        return list_to_return


    """
    kml_format takes self as it's only argument and returns a list of tuples or coordinate information in x,y format.
    ie - a .kml readable format
    """

    def kml_format(self):
        assert len(self.points) > 0
        tuple_list = [x.kml_tuple() for x in self.points]
        return tuple_list

    """
    Create_sides takes args and kwargs as it's arguments.  Args must be valid LinePath instances containing coordinate
    instances.  Both LinePath instance must be of equal length.  It does not return anything however it updates the 
    self.sides attribute to a list of kml readable tuples which are used to draw the 'sides' of the polygons.
    """
    def create_sides(self, linepath1: 'LinePath', linepath2: 'LinePath'):
        i = 0
        side_list = []
        # This if condition creates the sides up to the last coordinate,
        # else then creates the last side back to the first coordinate
        while i < len(linepath1.points):
            if i < len(linepath1.points) - 1:
                side_list.append(
                    [
                        (linepath1.points[i].longitude, linepath1.points[i].latitude,
                         linepath1.points[i].height),
                        (linepath1.points[i + 1].longitude, linepath1.points[i + 1].latitude,
                         linepath1.points[i + 1].height),
                        (linepath2.points[i + 1].longitude,
                         linepath2.points[i + 1].latitude,
                         linepath2.points[i + 1].height),
                        (linepath2.points[i].longitude,
                         linepath2.points[i].latitude,
                         linepath2.points[i].height)
                    ]
                )
                i += 1

            # When you get to the final coordinate and need to create side
            # back to the first coordinate, do this
            else:
                side_list.append(
                    [
                        (linepath1.points[i].longitude, linepath1.points[i].latitude,
                         linepath1.points[i].height),
                        (linepath1.points[0].longitude, linepath1.points[0].latitude,
                         linepath1.points[0].height),
                        (linepath2.points[0].longitude,
                         linepath2.points[0].latitude,
                         linepath2.points[0].height),
                        (linepath2.points[i].longitude,
                         linepath2.points[i].latitude,
                         linepath2.points[i].height)
                    ]
                )
                i += 1

        return side_list

    def create_layer_and_sides(self, height: float):
        new_line_path = LinePath(copy.deepcopy(self.points), height=height, sort=self.sort, origin=self.origin)
        return new_line_path, self.create_sides(new_line_path, self)
