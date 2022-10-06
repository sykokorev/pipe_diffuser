from mathlib.math import *
from mathlib.shape import Line


class LineInterpolation(Line):

    def __init__(self, points: list=[[0.0, 0.0], [1.0, 1.0]]):
        super().__init__(points=points)
        self.__points = points
        self.__num_lines = len(self.__points) - 1
        self.lines = [
                Line(points=[self.points[i-1], self.points[i]])
                for i in range(1, self.__num_lines+1)
            ]
        self.__lengths = [line.get_length() for line in self.lines]
        
    @property
    def num_lines(self):
        return self.__num_lines
    
    @property
    def lengths(self):
        return self.__lengths

    def get_length(self):
        return sum(self.__lengths)

    def interpolate(self, points: list):
        out = []
        for point in points:
            for line in self.lines:
                if line.first_point[0] <= point <= line.last_point[0]:
                    out.append(line.get_point(abscissa=point))
        return out
    
    def __repr__(self):
        lines = ''
        points_str = ''
        for point in self.points:
            for p in point:
                points_str += f'{round(p, 4)}\t'
            points_str += '\n'
        for line in self.lines:
            lines += f'{line}'
        return f'Points:\n{points_str}\n{lines}\n'
