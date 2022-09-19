from audioop import add
import math
from urllib.response import addinfo
import matplotlib.pyplot as plt
from mathlib.math import linspace
from mathlib.quaternion import Quaternion


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

    teta = math.radians(90)
    del_teta = linspace(0, teta, 45)
    x = 2
    derivatives = bezier.derivative(t=0.75)
    point1 = bezier.get_point(t=0.75)
    point2 = [p + (d / derivatives[0]) * (x - point1[0]) for p, d in zip(point1, derivatives)]

    P2 = DQ(
        D0=Quaternion(scalar=1.0, vector=[0.0, 0.0, 0.0]),
        D1=Quaternion(scalar=0.0, vector=point2)
    )

    P1 = DQ(
        D0=Quaternion(scalar=1.0, vector=[0.0, 0.0, 0.0]),
        D1=Quaternion(scalar=0.0, vector=point1)
    )

    
    dq_rot = DQ(
        D0=Quaternion(scalar=math.cos(teta/2), 
            vector=vc.scalar_vector(scalar=math.sin(teta/2), vector=vc.normed(vector=[1.0, 0.0, 0.0]))
        ),
        D1=Quaternion()
    )



    Pout = dq_rot.mult(P2).mult(dq_rot.conjugate())
    pout = vc.normed(vector=vc.addition(v1=P1.Dual.vector, v2=Pout.Dual.vector))
    p_per = [P1.Dual.vector, pout]

    # trajectory = []
    # for tetai in del_teta:
    #     dq_rot.Real.scalar=math.cos(tetai/2)
    #     dq_rot.Real.vector=


    Pab = DQ(
        D0=Quaternion(scalar=1.0, vector=[0.0, 0.0, 0.0]),
        D1=Quaternion(scalar=0.0, vector=[3.0, 3.0, 3.0])
    )

    P1 = DQ(
        D0=Quaternion(scalar=1.0, vector=[0.0, 0.0, 0.0]),
        D1=Quaternion(scalar=0.0, vector=[3.0, 3.0, 3.0])
    )

    P2 = Pab.mult(P1)
    print(P2)

    ########################################################################################

    # plot_data = pldata(data=coordinates)
    # fig, ax = plot_data.plt_3Dgraph()
    # plot_data.add_3Dgraph(ax=ax, data=[point1, point2])
    # plot_data.add_3Dgraph(ax=ax, data=p_per, marker='o', color='g')

    # plt.show()
