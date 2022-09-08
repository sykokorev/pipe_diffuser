import math

from mathlib.bezier import BezierThroughPoints as bezier
from mathlib.gaussian_quadrature import GQ as gq
from mathlib.shape import Circle, Line


class PipeDiffuser:
    def __init__(self, *args, **kwargs):
        self.__num_pipes = kwargs.get('num_pipes', 21)
        self.__rimp = kwargs.get('r_tan_imp')
        self.__xbeta = kwargs.get('xbeta', [])
        self.__xr = kwargs.get('xr', [])
        self.__length_star = kwargs.get('length_star', 0.0)
        self.__del_length_star = kwargs.get('del_length_star', 0.0)
        self.__rimp = kwargs.get('rimp', 0.0)
        self.__wh = kwargs.get('wh', [])
        self.__area = kwargs.get('area', [])
        self.__xteta = self.__calc_xteta(xbeta=self.__xbeta, xr=self.__xr)
        self.__mean_line: list = []
        self.__ml_bezier: object = None

    @property
    def num_pipes(self):
        return self.__num_pipes
    
    @property
    def rimp(self):
        return self.__rimp

    @property
    def xbeta(self):
        return self.__xbeta

    @property
    def xr(self):
        return self.__xr

    @property
    def length_star(self):
        return self.__length_star

    @property
    def del_length_star(self):
        return self.__del_length_star

    @property
    def xteta(self):
        return self.__xteta

    @property
    def mean_line(self):
        return self.__mean_line

    @property
    def area(self):
        return self.__area

    @property
    def wh(self):
        return self.__wh

    @num_pipes.setter
    def num_pipes(self, value: int):
        if isinstance(value, int):
            self.__num_pipes = value

    @rimp.setter
    def rimp(self, value: float):
        if isinstance(value, float):
            self.__rimp = value

    @xbeta.setter
    def xbeta(self, arr: list):
        if hasattr(arr, '__iter__'):
            if all([isinstance(item, float) for item in arr]):
                self.__xbeta = arr
    
    @length_star.setter
    def length_star(self, value: float):
        if isinstance(value, float):
            self.__length_star = value

    @del_length_star.setter
    def del_length_star(self, value: float):
        if isinstance(value, float):
            self.__del_length_star = value

    @xteta.setter
    def xteta(self, xbeta: list, xr: list):
        if hasattr(xbeta, '__iter__') and hasattr(xr, '__iter__'):
            if all([isinstance(item, float) for item in xbeta]):
                if all([isinstance(item, float) for item in xr]):
                    self.__calc_xteta(xbeta=xbeta, xr=xr)

    def __calc_xteta(self, xbeta: list, xr: list):

        teta0 = math.atan((self.length_star + self.del_length_star) / self.rimp)
        xteta = [[xr[0][0], teta0]]

        for i, (xri, xbetai) in enumerate(zip(xr[1:], xbeta[1:]), 1):
            dx = xri[0] - xr[i-1][0]
            teta = xr[i-1][1] * math.cos(xteta[i-1][1])
            teta -= dx * math.tan(math.radians(xbetai[1]))
            teta /= xri[1]
            teta = math.acos(teta)
            xteta.append([xri[0], teta])
        
        return xteta

    def compute_mean_line(self):
        
        self.__mean_line = [
            [xri[0], xri[1] * math.sin(tetai[1]), xri[1] * math.cos(tetai[1])]
            for xri, tetai in zip(self.__xr, self.__xteta)
        ]
        self.__ml_bezier = bezier(points=self.__mean_line)
        return self.__mean_line

    def get_mean_line_length(self):

        if self.__ml_bezier:
            length = self.__ml_bezier.length
            return length
        else:
            return 0.0

    def compute_cross_section(self, wh: float=1.0, area: float=1.0, num_points: int=40):

        h = 2 * (area / (wh - 1 + math.pi)) ** 0.5
        w = wh * h
        c1 = Circle(center=[-w/2+h/2, 0.0], radius=h/2)
        c2 = Circle(center=[w/2-h/2, 0.0], radius=h/2)
        
        if wh == 1:
            points = [
                *c1.get_points(a1=3*math.pi/2, a2=math.pi/2, num_points=int(num_points/2)),
                *c2.get_points(a1=math.pi/2, a2=-math.pi/2, num_points=int(num_points/2)),
            ]
        else:
            line1 = Line(points=[[-w/2+h/2, h/2], [w/2-h/2, h/2]])
            line2 = Line(points=[[w/2-h/2, -h/2], [-w/2+h/2, -h/2]])
            points = [
                *c1.get_points(a1=3*math.pi/2, a2=math.pi/2, num_points=int(num_points/4)),
                *line1.get_points(num_points=int(num_points/4)),
                *c2.get_points(a1=math.pi/2, a2=-math.pi/2, num_points=int(num_points/4)),
                *line2.get_points(num_points=int(num_points/4))
            ]

        return points
