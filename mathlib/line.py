from mathlib.math import *


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

    def __get_slope(self):
        if self.points[0][0] != self.points[1][0]:
            slope = [ 
                    (self.points[1][j] - self.points[0][j]) / (self.points[1][0] - self.points[0][0])
                    for j in range(self.spacial)
                ]
        else:
            slope = [0 for i in range(self.spacial)]
        return slope


class LineInterpolation(Line):

    def __init__(self, points: list=[[0.0, 0.0], [1.0, 1.0]]):
        super().__init__(points=points)
        self.__points = points
        self.__num_lines = len(self.__points) - 1
        self.lines = [
                Line(points=[self.points[i-1], self.points[i]])
                for i in range(1, self.__num_lines)
            ]
        
    @property
    def num_lines(self):
        return self.__num_lines

    def get_length(self):
        return sum(line.get_length() for line in self.lines)

    def interpolate(self, points: list):
        out = []
        
        for point in points:
            for line in self.lines:
                if line.first_point[0] <= point <= line.last_point[0]:
                    out.append(line.get_point(abscissa=point))

        return out

    def __lengths(self):
        return [line.get_length() for line in self.lines]
