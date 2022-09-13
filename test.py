import math
import numpy as np
import matplotlib.pyplot as plt
from mathlib.bezier import BezierThroughPoints
from mathlib.matrix import prt_mat, prt_vec
from mathlib.shape import *
from mathlib.math import *
from chart.chart import *
import mathlib.vector as vec
from mathlib.quaternion import Quaternion
from mathlib.dual_quaternion import DualQuaternion


if __name__ == "__main__":

    # Dual Quternion test
    # rot_axis = vec.normed(vector=[0.0, 0.0, 1.0])
    # rot_axis2 = vec.normed(vector=[0.0, 1.0, 0.0])
    # teta = math.radians(90)
    # teta2 = math.radians(90)

    # q0 = Quaternion(scalar=math.cos(teta/2), vector=vec.scalar_vector(scalar=math.sin(teta2/2), vector=rot_axis2))
    # q1 = Quaternion(scalar=math.cos(teta/2), vector=vec.scalar_vector(scalar=math.sin(teta/2), vector=rot_axis))
    # q2 = Quaternion(scalar=math.cos(teta2/2), vector=vec.scalar_vector(scalar=math.sin(teta2/2), vector=rot_axis2))

    # rot_dq1 = DualQuaternion(D0=q0, D1=q1)
    # rot_dq2 = DualQuaternion(D0=q1, D1=q2)

    # print('#'*50)
    # print('DQ1')
    # print(rot_dq1)
    # print('DQ2')
    # print(rot_dq2)
    # print('#'*50)

    # print('Addition DQ')
    # print(rot_dq1.addition(rot_dq2))
    # print('#'*50)
    # print('Multiplication DQ')
    # print(rot_dq1.mult(rot_dq2))
    # print('#'*50)

    # print('Conjugations')
    # print('Initial DQ')
    # print(rot_dq1)
    # print('Quternion conjugate')
    # print(rot_dq1.quaternion_conjugate())
    # print('Dual number conjugate')
    # print(rot_dq1.dual_number_conjugate())
    # print('Conjugate')
    # print(rot_dq1.conjugate())
    # print('#'*50)
    # print('Norm')
    # print(rot_dq1.norm)
    # print('#'*50)

    print('Test unit DQ')
    teta1 = math.radians(60)
    teta2 = math.radians(30)
    unit_axis1 = vec.normed(vec.scalar_vector(scalar=math.sin(teta1/2), vector=[1.0, 2.0, 3.0]))
    unit_axis2 = vec.normed(vec.scalar_vector(scalar=math.sin(teta2/2), vector=[2.0, 1.5, 2.5]))

    unit_q1 = Quaternion(scalar=math.cos(teta1/2), vector=unit_axis1)
    unit_q1.normed()
    unit_q2 = Quaternion(scalar=math.cos(teta2/2), vector=unit_axis2)
    unit_q2.normed()
    zero_q = Quaternion()

    unit_dq = DualQuaternion(D0=unit_q1, D1=unit_q2)

    print('Quaternion multiplication')
    print(f'{unit_q2.conjugate().mult(unit_q1)=}')
    print(f'{unit_q1.conjugate().mult(unit_q2)=}')
    print(f'{unit_q1.conjugate().mult(unit_q1)=}')

    print('##########Conjugate DQ##########')
    print(f'{unit_dq=}')
    print(f'{unit_dq.quaternion_conjugate()=}')
    print(f'{unit_dq.dual_number_conjugate()=}')
    print(f'{unit_dq.conjugate()=}')

    print('##########Pure Displacement##########')
    p1 = [3.0, 4.0, 5.0]
    p1_dq = DualQuaternion(D0=Quaternion(scalar=1.0, vector=[0.0, 0.0,0.0]), D1=Quaternion(scalar=0.0, vector=p1))

    displacement = [4, 2, 6]
    displacement = vec.scalar_vector(scalar=0.5, vector=displacement)
    dq = DualQuaternion(D0=Quaternion(scalar=1.0, vector=[0.0, 0.0, 0.0]), D1=Quaternion(scalar=0.0, vector=displacement))
    p2_dq = dq.mult(p1_dq).mult(dq.conjugate())
    print(f'End DQ:\t{p2_dq}\nInitial DQ:\t{p1_dq}\nDisplacement:\t{displacement}\n')

    print('##########Pure rotation##########')
    p1 = [3.0, 4.0, 5.0]
    p1_dq = DualQuaternion(D0=Quaternion(scalar=1.0, vector=[0.0, 0.0, 0.0]), D1=Quaternion(scalar=0.0, vector=p1))
    teta = math.radians(180)
    unit_axis = vec.normed(vector=[1.0, 0.0, 0.0])
    dq = DualQuaternion(
        D0=Quaternion(
            scalar=math.cos(teta/2), 
            vector=vec.scalar_vector(scalar=math.sin(teta/2), vector=unit_axis)),
        D1=Quaternion()
    )
    p2_dq = dq.mult(p1_dq).mult(dq.conjugate())
    trajectory = []

    for i, tetai in enumerate(linspace(0, teta, 18)):
        if i:
            tetai = tetai / i
        dq.D0.vector = vec.scalar_vector(scalar=math.sin(tetai/2), vector=unit_axis)
        dq.D0.scalar = math.cos(tetai/2)
        p2_dq = dq.mult(p1_dq).mult(dq.conjugate())
        trajectory.append(p2_dq.Dual.vector)
        p1_dq.D1.vector = p2_dq.Dual.vector

    for point in trajectory:
        print(point)
    print()

    print('##########Combine Displacement and Rotation##########')
    print()
    trajectory = []
    teta = math.radians(180)
    p1 = DualQuaternion(
        D0=Quaternion(scalar=1.0, vector=[0.0, 0.0, 0.0]), 
        D1=Quaternion(scalar=0.0, vector=[3.0, 4.0, 5.0])
    )
    d = vec.scalar_vector(scalar=0.5, vector=[4.0, 2.0, 6.0])
    unit_axis = vec.normed(vector=[1.0, 0.0, 0.0])
    axis = vec.scalar_vector(scalar=math.sin(teta/2), vector=unit_axis)

    Tr = DualQuaternion(
        D0=Quaternion(scalar=1.0, vector=[0.0, 0.0, 0.0]),
        D1=Quaternion(scalar=0.0, vector=d)
    )
    Rot = DualQuaternion(
        D0=Quaternion(scalar=math.cos(teta/2), vector=axis),
        D1=Quaternion()
    )
    print('##########Displacement then Rotation##########')
    p2 = Tr.mult(Rot).mult(p1).mult(Rot.conjugate()).mult(Tr.conjugate())
    print(p2)
    print('##########Rotation then Displacement##########')
    p2 = Rot.mult(Tr).mult(p1).mult(Tr.conjugate()).mult(Rot.conjugate())
    print(p2)

    num_points = 18
    d = vec.scalar_vector


    # Plotting
    # Pure Displacement
    print('########### Pure Displacement Test ###########')
    print('########### Displacement alond X axis ###########')
    p1 = DualQuaternion(D0=Quaternion(scalar=1.0, vector=[0.0, 0.0, 0.0]),
                        D1=Quaternion(scalar=0.0, vector=[2.0, 2.0, 2.0]))
    t_axis = [1.0, 0.0, 0.0]
    d = 2.0
    axis = vec.scalar_vector(scalar=d/2, vector=t_axis)
    Tr = DualQuaternion(
        D0=Quaternion(scalar=1.0, vector=[0.0, 0.0, 0.0]),
        D1=Quaternion(scalar=0.0, vector=axis)
    )
    p2 = Tr.mult(p1).mult(Tr.conjugate())
    print(f'Start point\t{p1}')
    print(f'End point\t{p2}')
    trajectory_x = [p1.Dual.vector, p2.Dual.vector]

    print('########### Displacement along Y axis ###########')
    t_axis = [0.0, 1.0, 0.0]
    axis = vec.scalar_vector(scalar=d/2, vector=t_axis)
    Tr.Dual.vector = axis
    p2 = Tr.mult(p1).mult(Tr.conjugate())
    print(f'Start point\t{p1}')
    print(f'End point\t{p2}')
    trajectory_y = [p1.Dual.vector, p2.Dual.vector]

    print('########### Displacement along Z axis ###########')
    t_axis = [0.0, 0.0, 1.0]
    axis = vec.scalar_vector(scalar=d/2, vector=t_axis)
    Tr.Dual.vector = axis
    p2 = Tr.mult(p1).mult(Tr.conjugate())
    print(f'Start point\t{p1}')
    print(f'End point\t{p2}')
    trajectory_z = [p1.Dual.vector, p2.Dual.vector]

    print('########### Displacement along XYZ axis ###########')
    t_axis = [1.0, 1.0, 1.0]
    axis = vec.scalar_vector(scalar=d/2, vector=t_axis)
    Tr.Dual.vector = axis
    p2 = Tr.mult(p1).mult(Tr.conjugate())
    print(f'Start point\t{p1}')
    print(f'End point\t{p2}')
    trajectory_xyz = [p1.Dual.vector, p2.Dual.vector]

    print('########### Arbitrary displacement ###########')
    p1.Dual.vector = [3.0, 4.0, 5.0]
    t_axis = [4.0, 2.0, 6.0]
    axis = vec.scalar_vector(scalar=0.5, vector=t_axis)
    Tr.Dual.vector = axis
    p2 = Tr.mult(p1).mult(Tr.conjugate())
    print(f'Start point\t{p1}')
    print(f'End point\t{p2}')
    trajectory = [p1.Dual.vector, p2.Dual.vector]
    displacement_axis = [[0]*3, vec.normed(t_axis)]


    # Trajectory Plotitng

    chart = PlotData(data=trajectory_x, label='X Displacement', marker='')
    fig, ax = chart.plt_3Dgraph()
    chart.add_3Dgraph(ax=ax, data=trajectory_y, color='r', label='Y Displacement')
    chart.add_3Dgraph(ax=ax, data=trajectory_z, color='y', label='Z Displacement')
    chart.add_3Dgraph(ax=ax, data=trajectory_xyz, color='m', label='XYZ Displacement')
    chart.add_3Dgraph(ax=ax, data=trajectory, color='g', label='Arbitrary Displacement')
    chart.add_3Dgraph(ax=ax, data=displacement_axis, color='k', label='Unitary axis')
    ax.legend()
    plt.show()
    