from ast import Index
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.ticker import AutoMinorLocator
from matplotlib.gridspec import GridSpec


class PlotData:

    """
    The class provides methods to create charts

    Methods
    -------
    plt_2Dgraph(data: np.array=np.zeros(shape=(0)))
        Plotting 2D chart
    add_2Dgraph(ax: matplotlib.pyplot.axis, data: np.array)
        Adding graph to an existing chart
    plt_3Dgraph(**kwargs)
        Plotting 3D chart
    add_3Dgraph(ax: matplotlib.pyplot.axis, data: np.array)
        add 3D graph to an existing chart
    """

    graphs = []

    def __init__(self, data: np.array([])=np.zeros(shape=1), *args, **kwargs):

        self.data = data
        self.title = kwargs.get('title', 'Chart')
        self.axis_labels = kwargs.get('axis_labels', ['X', 'Y', 'Z'])
        self.color = kwargs.get('color', 'b')
        self.line_style = kwargs.get('line_style', '-')
        self.marker = kwargs.get('marker', 'o')
        self.marker_color = kwargs.get('marker_color', 'b')
        self.annotate = kwargs.get('annotate')
        self.limits = kwargs.get('limits')
        self.major_ticks = kwargs.get('major_ticks')
        self.major_grid = kwargs.get('major_grid', True)
        self.minor_grid = kwargs.get('major_grid', True)
        self.label = kwargs.get('label')
        self.nrows = kwargs.get('nrows', 1)
        self.ncols = kwargs.get('ncols', 1)
        self.shared_axis = kwargs.get('shared_axis', [False, False])
        self.legend = kwargs.get('legend', False)

    def annotate_axes(self, fontsize=18, ha='center', va='center'):
        self.__ax.text(0.5, 0.5, self.annotate, 
                       transform=self.__ax.transAxes,
                       ha=ha, va=va, fontsize=fontsize)

    def __set_limits(self, ax, x, y):
        limits = np.array([
            np.round([0.95 * min(x), 1.05 * max(x)], 2),
            np.round([0.95 * min(y), 1.05 * max(y)], 2)
        ])
        ax.set_xlim(limits[0])
        ax.set_ylim(limits[1])
        return limits 

    def __set_major_ticks(self, limits):
        self.major_ticks = np.array([
            np.round(np.linspace(limits[0, 0], limits[0, 1], 5), 2),
            np.round(np.linspace(limits[1, 0], limits[1, 1], 5), 2)
        ])

    def add_2Dgraph(self, ax: plt.axis, data: np.array([]), **kwargs):

        x = [xi[0] for xi in data]
        y = [yi[0] for yi in data]

        if kwargs.get('limits'):
            limits = self.__set_limits(ax, x, y)

        if kwargs.get('major_ticks'):
            major_ticks = self.__set_major_ticks(ax, limits)

        params = {
            'color': kwargs.get('color', 'r'),
            'linestyle': kwargs.get('linestyle', '-'),
            'marker': kwargs.get('marker', ','),
            'markerfacecolor': kwargs.get('markerfacecolor', 'r'),
            'label': kwargs.get('label', f'Graph {self.graphs}')
        }

        line, = plt.plot(x, y, **params)
        self.graphs.append(line)
        ax.legend(handles=self.graphs)

    def add_3Dgraph(self, ax: plt.axis, data: np.array([]), **kwargs):

        try:
            x = [xi[0] for xi in data]
            y = [yi[1] for yi in data]
            z = [zi[2] for zi in data]
        except (IndexError, TypeError):
            x, y, z = data[0], data[1], data[2]

        params = {
            'color': kwargs.get('color', 'r'),
            'linestyle': kwargs.get('linestyle', '-'),
            'marker': kwargs.get('marker', ','),
            'markerfacecolor': kwargs.get('markerfacecolor', 'r'),
            'label': kwargs.get('label', f'Graph {self.graphs}')
        }

        ax.plot(x, y, z, **params)

    def plt_2Dgraph(self, data: np.array = np.zeros(shape=(0))):

        if not data.size:
            try:
                x = [xi[0] for xi in self.data]
                y = [yi[1] for yi in self.data]
            except (IndexError, TypeError):
                x = self.data[0]
                y = self.data[1]
        else:
            try:
                x = [xi[0] for xi in data]
                y = [yi[0] for yi in data]
            except (IndexError, TypeError):
                x = data[0]
                y = data[1]

        self.__fig, self.__ax = plt.subplots(
            sharex=self.shared_axis[0],
            sharey=self.shared_axis[1]
        )

        line, = self.__ax.plot(x, y, color=self.color, linestyle=self.line_style,
                      marker=self.marker, markerfacecolor=self.marker_color,
                      label=self.label)

        self.__ax.set(xlabel=self.axis_labels[0], ylabel=self.axis_labels[1],
                     title=self.title)
        
        if not self.limits:
            self.limits = self.__set_limits(self.__ax, x, y)

        if not self.major_ticks:
            self.__set_major_ticks(self.limits)

        self.__ax.set_xticks(self.major_ticks[0])
        self.__ax.set_yticks(self.major_ticks[1])
        
        self.__ax.xaxis.set_minor_locator(AutoMinorLocator())
        self.__ax.yaxis.set_minor_locator(AutoMinorLocator())
        
        self.__ax.tick_params(which='major', width=1, length=5)
        self.__ax.tick_params(which='minor', width=0.5, length=2)

        self.__ax.grid(visible=self.major_grid, which='major', lw=1, ls='-')
        self.__ax.grid(visible=self.minor_grid, which='minor', lw=0.5, ls='--')

        self.graphs.append(line)

        if self.legend:
            self.__ax.legend()

        return self.__fig, self.__ax

    def plt_3Dgraph(self, **kwargs):

        self.__fig = plt.figure()

        self.__ax = self.__fig.add_subplot(111, projection='3d')
        try:
            x = [xi[0] for xi in self.data]
            y = [yi[1] for yi in self.data]
            z = [zi[2] for zi in self.data]
        except (IndexError, TypeError):
            x, y, z = self.data[0], self.data[1], self.data[2]
        self.__ax.plot(x, y, z, label=self.label, **kwargs)

        return self.__fig, self.__ax
