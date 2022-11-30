import math
import numpy as np
import matplotlib.pyplot as plt

from matplotlib import figure
from ipywidgets import interact


@interact
def sinwave(c=1):

    p = np.linspace(0, 2*math.pi, 100)
    y = np.sin(p*c)

    plt.plot(p, y)
    plt.ylabel('sin(x)')
    plt.xlabel('x')
    plt.title('Sinwave function')
    return plt.figure()


if __name__ == "__main__":

    fig = sinwave()
    
