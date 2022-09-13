from mathlib.math import *
from mathlib.matrix import *
from mathlib.gaussian_quadrature import GQ as gq

class BaseBezier:

    def __init__(self, points: list, *args, **kwargs):
        self.__points = points
        self.__degree = len(self.__points) - 1
        self.__space_dimention = len(self.__points[0])
        self.__npoints = kwargs.get('npoints', 50)
        self.__first_point = self.__points[0]
        self.__last_point = self.__points[-1]

    @property
    def points(self):
        return self.__points

    @property
    def degree(self):
        return self.__degree

    @property
    def dimention(self):
        return self.__space_dimention

    @property
    def num_points(self):
        return self.__npoints

    @property
    def first_point(self):
        return self.__first_point

    @property
    def last_point(self):
        return self.__last_point

    def _binomial_coefficient(self, n: int, i: int) -> float:
        return factorial(n) / (factorial(i) * factorial(n - i))

    def _Bernstein_polynomial(self, n: int, i: int, t: float) -> float:
        return self._binomial_coefficient(n, i) * t ** i * (1 - t) ** (n - i)

    def _get_coordinates(self, n: int, t: float, points: list) -> list:
        coordinates = [0] * self.dimention

        for i in range(n + 1):
            for d in range(self.dimention):
                coordinates[d] += self._Bernstein_polynomial(n ,i, t) * points[i][d]

        return coordinates

    def get_polynomial_coefficients(self) -> list:

        c = []
        n = self.degree
        cols = self.dimention
        for j in range(0, n + 1):
            ci = [0] * cols
            binom = factorial(n) / factorial(n - j)
            for i in range(j + 1):
                polynom = ((-1) ** (i + j)) / (factorial(i) * factorial(j - i))
                for col in range(cols):
                    ci[col] += binom * polynom * self.points[i][col]
            c.append(ci)
        return c
                    
    def get_point(self, t: float=0) -> list:
        coef = self.get_polynomial_coefficients()
        point = coef[0]
        for i, c in enumerate(coef[1:], 1):
            for j, ci in enumerate(c):
                point[j] += ci * t ** i
        
        return point

    def get_points(self, t: list) -> list:
        return [self.get_point(ti) for ti in t]

    def get_length(self, n: int=5, t1: float=0.0, t2: float=1.0):
        w = gq[n][0]
        x = gq[n][1]
        length = 0.0
        for i in range(n):
            ti = (t2 - t1) * x[i] / 2 + (t2 - t1) / 2
            ft = sum([p ** 2 for p in self.derivative(t=ti)]) ** 0.5
            length += w[i] * ft
        length *= (t2 - t1) / 2
        return length

    def get_coordinates(self, npoints: int = 0, start: float=0.0, stop: float=1.0) -> list:
        if not npoints:
            npoints = self.num_points
        points = [0] * npoints
        t = linspace(start, stop, npoints)
        for i, ti in enumerate(t):
            points[i] = self._get_coordinates(self.degree, ti, self.points)
        
        return points

    def get_t(self, point: tuple([0, 0.0]), start: float=0.0, stop: float=1.0, eps: float=10**-3) -> float:

        left = self.get_point(t=0.0)[point[0]]
        rigth = self.get_point(t=1.0)[point[0]]

        t = linspace(start, stop, 1000)
        mid = self.get_point(t=t[int(len(t)/2)])[point[0]]

        if abs(left - point[1]) <= eps:
            return 0.0
        elif abs(rigth - point[1]) <= eps:
            return 1.0
        elif abs(mid - point[1]) <= eps:
            return t[int(len(t) / 2)]
        else:
            start = t[0] if mid > point[1] else t[int(len(t) / 2)]
            stop = t[int(len(t) / 2)] if mid > point[1] else t[len(t) - 1]
            return self.get_t(point, start=start, stop=stop)
        
    def derivative(self, t: float=0.0):
        n = self.degree
        if n <= 1:
            return 0.0
        else:
            point = [(1 - t) ** (n - 1) * (p2 - p1) for p1, p2 in zip(self.points[0], self.points[1])]

        for i in range(1, n):
            for d in range(self.dimention):
                point[d] += self._Bernstein_polynomial(n=(n - 1), i=i, t=t) * \
                    (self.points[i+1][d] - self.points[i][d])
        
        return [n * p for p in point]

    def get_length_point(self, length: float=0.0, t1: float = 0.0, t2: float = 1.0):
        eps = 10 ** -3

        if (length - 0) <= eps:
            return 0.0, self.get_point(t=0.0)
        elif abs(length - self.get_length()) <= eps:
            return 1.0, self.get_point(t=1.0)

        cur_len = 0.0
        count = 0.0
        max_count = 10 ** 5

        while abs(cur_len - length) > eps:
            if length > cur_len:
                t2 = t2 + 0.1 * t2
            elif length < cur_len:
                t2 = t2 - 0.1 * t2

            cur_len = self.get_length(t1=0.0, t2=t2)
            count += 1
            if count > max_count:
                return False
        return t2, self.get_point(t=t2)

    def __repr__(self):
        return 'BaseBezier\ndegree {degree};\n' \
               'Points: {points}\n'.format(degree=self.degree, points=self.points)


class BezierThroughPoints(BaseBezier):

    def __init__(self, points: list, *args, **kwargs):
        super().__init__(points=points, *args, **kwargs)
        self.curves = []
        self.__degree = 3
        self.__dim = 2 + (len(self.points) - 2) * 2
        self.__A = [[0] * self.__dim for d in range(self.__dim)]
        self.__B = [[0] * self.dimention for d in range(self.__dim)]
        self.__number_of_curves = len(self.points) - 1
        for points in self.__control_points():
            self.curves.append(BaseBezier(points=points))

        self.__first_point = self.curves[0].points[0]
        self.__last_point = self.curves[-1].points[-1]
        self.__curve_lengths = [curve.get_length() for curve in self.curves]
        self.__length = sum(self.__curve_lengths)

    @property
    def first_point(self):
        return self.__first_point

    @property
    def last_point(self):
        return self.__last_point

    @property
    def degree(self):
        return self.__degree

    @property
    def coordinates(self):
        return self.__coordinates

    @property
    def length(self):
        return self.__length

    @property
    def A(self) -> list:

        self.__A[0][:2] = [2, -1]
        self.__A[self.__dim - 1][self.__dim - 2:] = [-1, 2]

        j = 0
        for i in range(self.__dim):
            if j < self.__dim - 2:
                self.__A[i + 1][j + 1 : j + 3] = [1, 1]
                self.__A[i + int(self.__dim / 2)][j : j + 4] = [1, -2, 2, -1]
            j += 2

        return self.__A

    @property
    def B(self) -> list:

        self.__B[0] = self.points[0]
        self.__B[self.__dim - 1] = self.points[len(self.points) - 1]
        self.__B[1:len(self.points) - 1] = [
            [2 * p[i] for i in range(self.dimention)] for p in self.points[1:len(self.points) - 1]
            ]

        return self.__B

    @property
    def num_curves(self):
        return self.__number_of_curves

    def get_point(self, point: tuple=([0, 0.0])) -> float:

        idx = self.__get_curve_idx(point=point)
        if idx >= 0:
            t = self.curves[idx].get_t(point=(point[0], point[1]))
            curve = self.curves[idx]
            point = curve.get_point(t=t)
            return (t, point)
        else:
            return -1

    def interpolate(self, points: tuple([0, list])) -> list:

        curve_indices = [self.__get_curve_idx(point=(points[0], p)) for p in points[1]]
        out = []

        for i, index in enumerate(curve_indices):
            if index >= 0:
                t = self.curves[index].get_t(point=(points[0], points[1][i]))
                out.append(self.curves[index].get_point(t=t))

        return out

    def norm_length_point(self, norm_length: float=0.0) -> list:

        length = self.length * norm_length
        idx, ln = self.__get_curve_length_idx(length=length)

        if idx == -1:
            return -1
        else:
            return self.curves[idx].get_length_point(length=ln)

    def get_coordinates(self, npoints: int = 0) -> list:

        if not npoints:
            npoints = self.num_points

        coordinates = []

        for curve in self.__control_points():
            coordinates.append(curve[0])
            for t in linspace(0 + 1 / npoints, 1 - 1 / npoints, npoints):
                coordinates.append(self._get_coordinates(self.degree, t, curve))
            
        coordinates.append(self.points[-1])

        return coordinates

    def derivatives(self, norm_length: float=0.0) -> list:
        length = norm_length * self.length
        idx, ln = self.__get_curve_length_idx(length=length)
        point = self.curves[idx].get_length_point(length=ln)
        t = self.curves[idx].get_t(point=(0, point[1][0]))
        return self.curves[idx].derivative(t=t)

    def __get_curve_length_idx(self, length: float):
        lengths = [c.get_length() for c in self.curves]
        l = 0.0
        for i, ln in enumerate(lengths):
            l += ln
            if l >= length:
                return i, length - sum(lengths[:i])

        return -1, -1

    def __get_curve_idx(self, point: tuple):
        curve_points = [curve.first_point for curve in self.curves]
        curve_points.append(self.curves[-1].last_point)
        idx = span(point[1], list(zip(*curve_points))[point[0]])
        return idx

    def _get_coordinates(self, n, t, points) -> list:
        return super()._get_coordinates(n, t, points)

    def _Bernstein_polynomial(self, n, i, t) -> float:
        return super()._Bernstein_polynomial(n, i, t)

    def _binomial_coefficient(self, n, i) -> float:
        return super()._binomial_coefficient(n, i)
    
    def __control_points(self) -> list:

        cp = matmul(inverse(self.A), self.B)
        control_points = []

        for i in range(self.num_curves):
            control_points.append([[point for point in self.points[i]],
            [point for point in cp[2 * i:2 * i + 2]], [point for point in self.points[i + 1]]])

        return control_points
