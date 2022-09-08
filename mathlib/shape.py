import math

from mathlib.math import linspace


class Line:

    def __init__(self, points: list=[[0.0, 0.0], [1.0, 1.0]]):
        self.__points = points
        self.__spacial = len(self.__points[0])
        self.__first_point = self.__points[0]
        self.__last_point = self.__points[-1]
        self.__slope = self.__get_slope()


    @property
    def points(self):
        return self.__points

    @property
    def spacial(self):
        return self.__spacial

    @property
    def first_point(self):
        return self.__first_point

    @property
    def last_point(self):
        return self.__last_point

    @property
    def slope(self):
        return self.__slope

    @points.setter
    def points(self, pts):
        if hasattr(pts, '__iter__'):
            if all([isinstance(p, float) for p in pts]):
                self.__init__(points=pts)

    def get_point(self, abscissa: float):
        return [
            abscissa,
            *[self.points[0][j] + self.slope[j] * (abscissa - self.points[0][0]) 
            for j in range(1, self.spacial)]
        ]

    def get_length(self):
        ln = [(self.points[0][j] - self.points[1][j]) ** 2 for j in range(self.spacial)]
        return sum(ln) ** 0.5

    def get_point_length(self, length: float=0.0):
        m = length / self.get_length()
        point = [[
            self.points[0][j] + m * (self.points[1][j] - self.points[0][j])
            ] for j in range(self.spacial)]
        return point

    def interpolate(self, abscissa: list):

        if self.points[0][0] != self.points[1][0]:
            slope = [ 
                    (self.points[1][j] - self.points[0][j]) / (self.points[1][0] - self.points[0][0])
                    for j in range(self.spacial)
                ]
        else:
            slope = [0 for i in range(self.spacial)]
        out = []

        for x in abscissa:
            out.append(
                [x, *[self.points[0][j] + (x - self.points[0][0]) * slope[j] for j in range(1, self.spacial)]]
            )

        return out

    def get_points(self, num_points: int=10):
        t = linspace(0.0, 1.0, num_points=num_points)
        res = []
        for ti in t:
            res.append([
                self.__points[0][j] + ti * (self.__points[1][j] - self.__points[0][j])
                for j in range(self.__spacial)
            ])
        return res

    def __get_slope(self):
        if self.points[0][0] != self.points[1][0]:
            slope = [ 
                    (self.points[1][j] - self.points[0][j]) / (self.points[1][0] - self.points[0][0])
                    for j in range(self.spacial)
                ]
        else:
            slope = [0 for i in range(self.spacial)]
        return slope


class Shape:
    def __init__(self, center: list):
        self.__cp = center

    @property
    def center_point(self):
        return self.__cp

    @center_point.setter
    def center_point(self, value: list):
        if hasattr(value, '__iter__'):
            if all([isinstance(item, float) for item in value]):
                self.__cp = value

    
class Circle(Shape):
    def __init__(self, center: list, radius: float):
        super().__init__(center=center)
        self.__radius = radius

    @property
    def radius(self):
        return self.__radius
    
    @radius.setter
    def radius(self, radius):
        if isinstance(radius, float):
            self.__radius = radius

    def get_point(self, angle: float) -> list:
        return [self.center_point[0] + self.__radius * math.cos(angle),
                self.center_point[1] + self.__radius * math.sin(angle)
            ]

    def get_points(self, a1: float, a2: float, num_points: int) -> list:
        return [[self.center_point[0] + self.__radius * math.cos(a),
                 self.center_point[1] + self.__radius * math.sin(a)]
                 for a in linspace(a1, a2, num_points)]

    def get_perimeter(self) -> float:
        return 2 * math.pi * self.__radius

    def get_area(self) -> float:
        return math.pi * self.__radius ** 2

    def get_segment_perimeter(self, angle: float) -> float:
        return self.__radius * angle

    def get_segment_area(self, angle: float) -> float:
        return ((angle - math.sin(angle))  * self.__radius ** 2) / 2

    def get_chord_length(self, angle: float) -> float:
        return 2 * self.__radius * math.sin(angle)
    
    def get_chord_hight(self, angle: float) -> float:
        return self.__radius - (self.__radius ** 2 - (self.get_chord_length(angle=angle) ** 2) / 4) ** 0.5


class Rectangle(Shape):
    def __init__(self, center: list, heigth: float, width: float):
        super().__init__(center=center)
        self.__height = heigth
        self.__width = width

    @property
    def height(self):
        return self.__height

    @property
    def width(self):
        return self.__width

    @height.setter
    def height(self, h: float):
        if isinstance(h, float):
            self.__height = h

    @width.setter
    def width(self, w: float):
        if isinstance(w, float):
            self.__width = w

    def get_perimeter(self):
        return 2 * self.__height + 2 * self.__width

    def get_area(self):
        return self.__height * self.__width
