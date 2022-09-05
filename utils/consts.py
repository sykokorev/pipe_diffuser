import numpy as np
import math

GRAPH_COLORS = [
    'b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'
]
GRAPH_LINE_STYLE = [
    '-', '--', '-.', ':'
]
GRAPH_MARKERS = [
    '.', ',', 'o', 'v', '^', '<', '>', '1', '2', '3', '4', 
    's', 'p', '*', 'h', 'H', '+', 'x', 'D', 'd', '|', '_'
]

USC_SI = {
    'length': 0.0254
}

def RX(teta: float):
    return np.array([
        [1, 0, 0],
        [0, math.cos(teta), (-1) * math.sin(teta)],
        [0, math.sin(teta), math.cos(teta)]
    ])

def RY(teta):
    return np.array([
        [math.cos(teta), 0, math.sin(teta)],
        [0, 1, 0],
        [(-1) * math.sin(teta), 0, math.cos(teta)]
    ])