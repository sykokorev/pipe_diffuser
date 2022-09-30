import math
from re import A

from mathlib.dual_quaternion import DualQuaternion as DQ
from mathlib.quaternion import Quaternion as Q
from mathlib.vector import scalar_vector

from utils.utils import check_points
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
        self.__mean_line = []
        self.__twist = kwargs.get('twist', [])
        self.__lengths = kwargs.get('lengths', [])
        self.__cross_sections = []
        self.__ml_bezier = None

    @property
    def lengths(self):
        return self.__lengths

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

    @property
    def twist(self):
        return self.__twist

    @property
    def cross_sections(self):
        return self.__cross_sections

    @property
    def bezier_mean_line(self):
        return self.__ml_bezier

    @lengths.setter
    def lengths(self, points: list):
        if hasattr(points, '__iter__') and check_points(points=points):
            self.__lengths = points

    @area.setter
    def area(self, points: list):
        if hasattr(points, '__iter__') and check_points(points=points):
            self.__area = points

    @wh.setter
    def wh (self, points: list):
        if hasattr(points, '__iter__') and check_points(points=points):
            self.__wh = points

    @twist.setter
    def twist(self, points: list):
        if hasattr(points, '__iter__') and check_points(points=points):
            self.__twist = points

    @num_pipes.setter
    def num_pipes(self, value: int):
        if isinstance(value, int):
            self.__num_pipes = value

    @rimp.setter
    def rimp(self, value: float):
        if isinstance(value, float):
            self.__rimp = value

    @xbeta.setter
    def xbeta(self, points: list):
        if hasattr(points, '__iter__') and check_points(points=points):
            self.__xbeta = points
    
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
            if check_points(points=xbeta) and check_points(points=xr):
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

    def compute_cross_section(self, wh: float=1.0, area: float=1.0):

        h = (area / (wh - 1 + math.pi / 4)) ** 0.5
        w = wh * h
        c1 = Circle(center=[-w/2+h/2, 0.0, 0.0], radius=h/2)
        c2 = Circle(center=[w/2-h/2, 0.0, 0.0], radius=h/2)
        cross_section = []

        if wh == 1:
            cross_section.append([
                point for point in c1.get_points(
                    a1=3*math.pi/2 - math.radians(5), a2=math.pi/2 + math.radians(5),
                    num_points=3)
            ])
            cross_section.append([
                point for point in c1.get_points(
                    a1=math.pi/2 + math.radians(5), a2=math.pi/2 - math.radians(5),
                    num_points=2)
            ])
            cross_section.append([
                point for point in c2.get_points(
                    a1=math.pi/2 - math.radians(5), a2=-math.pi/2 + math.radians(5),
                    num_points=3)
            ])
            cross_section.append([
                point for point in c2.get_points(
                    a1=-math.pi/2 + math.radians(5), a2=3*math.pi/2 - math.radians(5),
                    num_points=2)
            ])
        else:
            line1 = Line(points=[[-w/2+h/2, h/2, 0.0], [w/2-h/2, h/2, 0.0]])
            line2 = Line(points=[[w/2-h/2, -h/2, 0.0], [-w/2+h/2, -h/2, 0.0]])
            cross_section.append([
                point for point in c1.get_points(a1=3*math.pi/2, a2=math.pi/2, num_points=3)
            ])
            cross_section.append([line1.first_point, line1.last_point])
            cross_section.append([
                point for point in c2.get_points(a1=math.pi/2, a2=-math.pi/2, num_points=3)
            ])
            cross_section.append([line2.first_point, line2.last_point])
        
        return cross_section
            
    def compute_cross_sections(self, wh: list=[], area: list=[], lengths: list=[]):

        if not wh or hasattr(wh, '__iter__') or check_points(points=wh):
            wh = self.wh
        
        if not area or hasattr(area, '__iter__') or check_points(points=area):
            area = self.area

        if not area or hasattr(lengths, '__iter__') or check_points(points=lengths):
            lengths = self.lengths

        self.__cross_sections = []
        derivatives = self.__ml_bezier.derivatives(norm_length=[l/lengths[-1] for l in lengths])
        tetaY = math.radians(90)

        Tr = DQ(D0=Q(scalar=1.0, vector=[0.0, 0.0, 0.0]), D1=Q())
        RotX = DQ(D0=Q(), D1=Q())
        RotY = DQ(D0=Q(), D1=Q())
        RotZ = DQ(D0=Q(), D1=Q())
        PointDQ = DQ(D0=Q(scalar=1.0, vector=[0.0, 0.0, 0.0]), D1=Q())

        for wh, area, twist, d, lenght in zip(
                [round(whi[1], 5) for whi in self.wh], 
                [round(areai[1], 5) for areai in self.area],
                [round(twisti[1], 5) for twisti in self.twist],
                derivatives,
                self.lengths
            ):
            dx, dy, dz = round(d[0], 5), round(d[1], 5), round(d[2], 5)

            if not dx:
                dzdx, dydxdz = round(-math.pi / 4, 4), round(math.pi / 2, 4)
            else:
                dzdx = round(math.atan(dz / dx), 4)
                dydxdz = round(math.atan(dy / (dx ** 2 + dz ** 2) ** 0.5), 4)

            point = self.__ml_bezier.norm_length_point(norm_length=(lenght/self.lengths[-1]))[1]

            Tr.Dual.vector = scalar_vector(scalar=0.5, vector=point)

            RotY.Real.scalar = math.cos(tetaY / 2 + dzdx / 2)
            RotY.Real.vector = scalar_vector(scalar=math.sin(tetaY / 2 + dzdx / 2), vector=[0.0, 1.0, 0.0])

            RotZ.Real.scalar = math.cos(dydxdz / 2)
            RotZ.Real.vector = scalar_vector(scalar=math.sin(dydxdz / 2), vector=[-1.0, 0.0, 0.0])

            RotX.Real.scalar = math.cos(twist / 2)
            RotX.Real.vector = scalar_vector(scalar=math.sin(twist / 2), vector=[0.0, 0.0, 1.0])

            ResDQ = RotX.mult(RotZ).mult(RotY).mult(Tr)
            ResDQ_conj = ResDQ.conjugate()
            points = []

            for shape in self.compute_cross_section(wh=wh, area=area):
                point = []
                for pt in shape:
                    PointDQ.Dual.vector = pt
                    point.append(ResDQ_conj.mult(PointDQ).mult(ResDQ).Dual.vector)
                points.append(point)

            self.__cross_sections.append([point, points])

        return self.__cross_sections

    def get_tangents(self, norm_length: list=[0.0, 1.0]):

        derivatives =  self.__ml_bezier.derivatives(norm_length=norm_length)
        return derivatives
