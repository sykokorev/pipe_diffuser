from audioop import add
import math
import matplotlib.pyplot as plt
from mathlib.math import linspace
from mathlib.quaternion import Quaternion as Q


import mathlib.vector as vc
import mathlib.matrix as mt

from mathlib.dual_quaternion import DualQuaternion as DQ
from mathlib.shape import Line
from mathlib.bezier import BaseBezier
from chart.chart import PlotData as pldata


if __name__ == "__main__":

    points = [
        [1.5, 1.0, 1.5],
        [2.0, 2.0, 2.0],
        [3.0, 3.0, 3.0],
        [1.5, 4.0, 1.5]
    ]

    bezier = BaseBezier(points=points)
    coordinates = bezier.get_coordinates()

    x = 2
    x2 = 3

    derivatives = bezier.derivative(t=0.5)
    point1 = bezier.get_point(t=0.5)

    point2 = [p + (d / derivatives[0]) * (x - point1[0]) for p, d in zip(point1, derivatives)]
    point3 = [p + (d / derivatives[0]) * (x2 - point1[0]) for p, d in zip(point1, derivatives)]

    alfa = math.atan(derivatives[1] / derivatives[0])
    beta = math.atan(derivatives[2] / derivatives[0])
    gamma = math.atan(derivatives[2] / (derivatives[1] ** 2 + derivatives[0] ** 2) ** 0.5)

    base_xaxis = [1.0, 0.0, 0.0]
    dq_base_xaxis = DQ(
        D0=Q(scalar=1.0, vector=[0.0, 0.0, 0.0]),
        D1=Q(scalar=0.0, vector=base_xaxis)
    )
    RotZ = DQ(
        D0=Q(scalar=math.cos(alfa/2), vector=vc.scalar_vector(scalar=math.sin(alfa/2), vector=[0.0, 0.0, -1.0])),
        D1=Q()
    )
    RotY = DQ(
        D0=Q(scalar=math.cos(beta/2), vector=vc.scalar_vector(scalar=math.sin(beta/2), vector=[0.0, 1.0, 0.0])),
        D1=Q()
    )
    RotYGamma = DQ(
        D0=Q(scalar=math.cos(gamma/2), vector=vc.scalar_vector(scalar=math.sin(gamma/2), vector=[0.0, 1.0, 0.0])),
        D1=Q()
    )
    Tr = DQ(
        D0=Q(scalar=1.0, vector=[0.0, 0.0, 0.0]),
        D1=Q(scalar=0.0, vector=vc.scalar_vector(scalar=0.5, vector=point1))
    )

    ResDQ = RotYGamma.mult(RotZ).mult(Tr)
    ResDQ_conj = ResDQ.conjugate()

    dq_point_transform = ResDQ_conj.mult(dq_base_xaxis).mult(ResDQ)
    point_transf = dq_point_transform.Dual.vector


    teta = math.radians(45)
    RotZteta = DQ(
        D0=Q(scalar=math.cos(teta/2), 
        vector=vc.scalar_vector(scalar=math.sin(teta/2), vector=[0.0, 0.0, -1.0])),
        D1=Q()
    )
    RotXteta = DQ(
        D0=Q(scalar=math.cos(teta/2), 
        vector=vc.scalar_vector(scalar=math.sin(teta/2), vector=[0.0, 1.0, 0.0])),
        D1=Q()
    )
    Trteta = DQ(
        D0=Q(scalar=1.0, vector=[0.0, 0.0, 0.0]),
        D1=Q(scalar=0.0, vector=vc.scalar_vector(scalar=0.5, vector=[1.0, 1.0, 1.0]))
    )

    DQResTeta = RotZteta.mult(RotXteta)#.mult(Trteta)
    DQResTeta_conj = DQResTeta.conjugate()
    point_teta = DQResTeta_conj.mult(dq_base_xaxis).mult(DQResTeta).Dual.vector

    ########################################################################################

    plot_data = pldata(data=coordinates)
    fig, ax = plot_data.plt_3Dgraph()
    plot_data.add_3Dgraph(ax=ax, data=[point2, point3])
    # plot_data.add_3Dgraph(ax=ax, data=[[0.0, 0.0, 0.0], point_teta], marker='o', color='r')
    plot_data.add_3Dgraph(ax=ax, data=[[0.0, 0.0, 0.0], base_xaxis], marker='s', color='g')
    plot_data.add_3Dgraph(ax=ax, data=[point1, point_transf], marker='o', color='g')

    plt.show()
