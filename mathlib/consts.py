import math

def RX(teta: float):
    return [
        [1, 0, 0],
        [0, math.cos(teta), (-1) * math.sin(teta)],
        [0, math.sin(teta), math.cos(teta)]
    ]

def RY(teta):
    return [
        [math.cos(teta), 0, math.sin(teta)],
        [0, 1, 0],
        [(-1) * math.sin(teta), 0, math.cos(teta)]
    ]
