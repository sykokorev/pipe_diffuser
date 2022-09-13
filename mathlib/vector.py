import mathlib.matrix as matrix


def dot(v1: list, v2: list) -> float:
    return sum([v1 * v2 for v1, v2 in zip(v1, v2)])


def cross(v1: list, v2: list) -> list:
    return [
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0]
    ]


def conjugate(vector: list) -> list:
    return [(-1) * v for v in vector]


def transpose(vector: list) -> list:
    return [[v] for v in vector]


def conj_trans(vector: list) -> list:
    return [[(-1) * v] for v in vector]


def outer(v1: list, v2: list) -> list:

    out = []
    for v in v1:
        out.append([v * (-1) * u for u in v2])
    
    return out


def wedge(v1: list, v2: list):

    u1 = outer(v1, v2)
    u2 = outer(v2, v1)
    for i, ui in enumerate(u2):
        u2[i] = [(-1) * uj for uj in ui]

    out = []
    for u1i, u2i in zip(u1 , u2):
        out.append([u1j + u2j for u1j, u2j in zip(u1i, u2i)])
    
    return out

def geometric(v1: list, v2: list):
    vdot = dot(v1=v1, v2=v2)
    vwedge = wedge(v1=v1, v2=v2)
    return matrix.scalar_addition(scalar=vdot, matrix=vwedge)


def magnitude(vector: list) -> list:
    return sum([vi ** 2 for vi in vector]) ** 0.5


def normed(vector: list) -> list:
    d = magnitude(vector)
    return [vi/d for vi in vector]


def scalar_vector(scalar: float, vector: list) -> list:
    return [vi * scalar for vi in vector]


def addition(v1: list, v2: list) -> list:
    return [v1i + v2i for v1i, v2i in zip(v1, v2)]


def scalar_addition(scalar: float, vector: list):
    return [vi + scalar for vi in vector]


def substraction(v1: list, v2: list) -> list:
    return [v1i * (-1) * v2i for v1i, v2i in zip(v1, v2)]
