import sys
import os
import logging
import subprocess
import json
import math
import tkinter as tk
import matplotlib.pyplot as plt

import utils.p1112_parser as p1112

from mathlib.math import *
from mathlib.bezier import *
from mathlib.line_interpolation import LineInterpolation
from diffuser.pipe_diffuser import PipeDiffuser as diffuser

from gui.gui import *
from utils.utils import find_nx_journal_run, select_file

from chart.chart import PlotData


if __name__ == "__main__":

    # GUI
    font = ("Helvetica", 14)
    root = tk.Tk()
    window = GUI(master=root)
    root.mainloop()
    indata_file = window.indata_file
    saveas = window.saveas
    num_sec = window.num_sec
    
    if not num_sec:
        tk.messagebox.showerror("showerror", "Number of section can't be equal 0")
        sys.exit(-1)

    units = 25.4

    logger = logging.getLogger(__name__)
    logger_file = os.path.join(os.path.split(saveas)[0], 'diffuser.log')

    if os.path.exists(logger_file):
        os.remove(logger_file)
    logging.basicConfig(filename=logger_file, level=logging.DEBUG)

    outdata_dir = os.path.join(os.path.split(saveas)[0], 'outdata')
    
    if not os.path.exists(outdata_dir):
        try:
            os.mkdir(outdata_dir)
        except FileExistsError as ex:
            msg = 'Directory has not been created an error occurs {ex}'
            logger.exception(msg)

    if not (os.path.exists(indata_file)):
        msg = 'File {file} doesn\'t exist'.format(file=os.path.abspath(indata_file))
        logger.error(msg)
        sys.exit(msg)

    # Parsing p1112 file
    # Input parameters
    indata, exception = p1112.input_parameters_p1112(in_file=indata_file)
    if not indata:
        msg = 'While parsing input parameters an error occurred {ex}'.format(ex=exception)
        logger.error(msg)
        sys.exit(msg)

    # Distributions
    # Data for mean line
    xr, exception = p1112.distribution(in_file=indata_file, string=r'x-r\s+\w+')
    if not exception:
        msg = 'X-R distribution has not been found. Input data will be applied.'
        logger.info(msg)

    xbeta, exeption = p1112.distribution(in_file=indata_file, string=r'x-beta\s+\w+')
    if not exception:
        msg = 'X-BETA distribution has not been found. Input data will be applied.'
        logger.info(msg)

    # Data for cross section
    wh, exeption = p1112.distribution(in_file=indata_file, string=r'w\W+h\s+\w+')
    if not exception:
        msg = 'WH distribution has not been found. Input data will be applied.'
        logger.info(msg)

    area, exception = p1112.distribution(in_file=indata_file, string=r'area\s+\w+')
    if not exception:
        msg = 'Area distribution has not been found. Input data will be applied.'
        logger.info(msg)

    twist, exception = p1112.distribution(in_file=indata_file, string=r'twist\s+\w+')
    if not exception:
        msg = 'Twist distribution has not been found. Input data will be applied.'
        logger.info(msg)

    # x linear distribution
    x0, x1 = xr[0][0], xr[-1][0]
    x = linspace(x0, x1, 100)
    xr_bezier = BezierThroughPoints(points=xr, npoints=2)
    xbeta_bezier = BezierThroughPoints(points=xbeta, npoints=2)
    wh_line = LineInterpolation(points=wh)
    area_line = LineInterpolation(points=area)
    twist_line = LineInterpolation(points=twist)

    norm_length = linspace(start=0.0, stop=1.0, num_points=num_sec)
    xr_points = [xr_bezier.norm_length_point(ni)[1] for ni in norm_length]
    xr_points = [[abs(round(xri[0], 4)), abs(round(xri[1], 4))] for xri in xr_points]

    xi = [p[0] for p in xr_points]
    xbeta_points = xbeta_bezier.interpolate(points=(0, xi))
    xbeta_points = [[round(b[0], 4), round(b[1], 4)] for b in xbeta_points]

    diffuser_params = {
        'xr': xr_points,
        'xbeta': xbeta_points,
        'length_star': float(indata['len_star']),
        'del_length_star': float(indata['del_len_star']),
        'rimp': float(indata['imp_tan_rad'])
    }

    pipe_diffuser = diffuser(**diffuser_params)
    mean_line = pipe_diffuser.compute_mean_line()
    mean_line = [[round(p[0], 4), round(p[1], 4), round(p[2], 4)] for p in mean_line]
    mean_line_length = pipe_diffuser.get_mean_line_length()
    length = [mean_line_length * nl for nl in norm_length]

    point = xbeta_bezier.get_point(point=(0, 3.5))
    wh_points = wh_line.interpolate(points=length)
    area_points = area_line.interpolate(points=length)
    twist_points = twist_line.interpolate(points=length)
    pipe_diffuser.lengths = length
    pipe_diffuser.wh = wh_points
    pipe_diffuser.area = area_points
    pipe_diffuser.twist = twist_points

    cross_sections = pipe_diffuser.compute_cross_sections()

    json_outdata = {
        "twist": twist_points,  
        "mean_line": mean_line,
        "cross_sections": cross_sections,
        "prt": os.path.normpath(saveas)
    }

    prt_file_name = os.path.splitext(os.path.split(saveas)[1])[0]
    outdata_file = os.path.join(outdata_dir, f'{prt_file_name}_json_data.json')
    mean_line_file = os.path.join(outdata_dir, f'{prt_file_name}_mean_line.dat')
    cross_sections_file = os.path.join(outdata_dir, f'{prt_file_name}_cross_sections.dat')

    with open(mean_line_file, 'w') as f:
        for point in mean_line:
            f.write(
                f'{round(point[0] * units, 4)},{round(point[1] * units, 4)},' \
                f'{round(point[2] * units, 4)}\n'
            )

    with open(cross_sections_file, 'w') as f:
        for si, section in enumerate(cross_sections, 1):
            f.write(f'Section {si}\n')
            for i, shape in enumerate(section[1]):
                if i == 0 or i == 2:
                    f.write('Arc\n')
                else:
                    f.write('Line\n')
                for points in shape:
                    f.write(
                        f'{round(points[0] * units, 4)},{round(points[1] * units, 4)},' \
                        f'{round(points[2] * units, 4)}\n'
                    )

    with open(outdata_file, 'w') as fo:
        json.dump(json_outdata, fo)

    nx_journal_run = find_nx_journal_run()

    if nx_journal_run:
        command = [
            nx_journal_run, "nx_builder.py", 
            '-args', os.path.normpath(os.path.abspath(outdata_file))
        ]
        code = subprocess.run(command)
    else:
        msg = "NX run journal file was not found\n. Please check if NX is installed.\n"
        logger.error(msg)
        tk.messagebox.showerror("showerror", msg)
        of_params = {
            'filetypes': ('NX run journal file', 'run_journal.exe'),
            'title': 'Open NX run journal file'
        }
        nx_journal_run = select_file(**of_params)
        if not nx_journal_run:
            sys.exit(-1)
        else:
            command = [
            nx_journal_run, ".nx_builder.py", 
            '-args', os.path.normpath(os.path.abspath(outdata_file))
            ]
            code = subprocess.run(command)

    # Create charts
    pic_dir = os.path.join(outdata_dir, 'pictures')
    if not os.path.exists(pic_dir):
        try:
            os.mkdir(pic_dir)
        except FileExistsError as ex:
            msg = 'Directory has not been created an error occurs {ex}'
            logger.exception(msg)

    # Norm Area (Ai/A1) distriburtion
    a1 = area_points[0][1]
    a_norm_distr = [[nl, a[1] / a1] for a, nl in zip(area_points, norm_length)]
    fn = os.path.join(pic_dir, f'{prt_file_name}_area_dist.jpg')

    x_major_ticks = [a[1] for a in a_norm_distr]
    chart = PlotData(data=a_norm_distr, 
        marker='s', color='b', markerfacecolor='b',
        title='Norm Length vs Norm Area (Ai/A1)', axis_labels=['Norm length', 'Norm Area'],
        major_ticks=[linspace(0.0, 1.0, 11), linspace(1, math.ceil(max(x_major_ticks)), 11)]
    )
    fig, ax = chart.plt_2Dgraph()
    fig.set_size_inches(10, 10)
    plt.savefig(fn, dpi=300, bbox_inches="tight", pad_inches=1)

    # ECA
    fn = os.path.join(pic_dir, f'{prt_file_name}_eca.jpg')
    eca = [
        [nl, (2 * math.degrees(math.atan((ai1[1] ** 0.5 - ai[1] ** 0.5) / math.pi ** 0.5) / (li1 - li) ))]
        for ai1, ai, li1, li, nl in zip(area_points[1:], area_points, length[1:], length, norm_length)
    ]
    x_major_ticks = [e[1] for e in eca]
    chart = PlotData(
        data=eca, marker_color='r',
        marker='s', color='r', markerfacecolor='r',
        title='Norm Length vs ECA(LOC)', axis_labels=['Norm Length', 'ECA(LOC)'],
        major_ticks=[
            linspace(0.0, 1.0, 11), 
            linspace(math.floor(min(x_major_ticks)), math.ceil(max(x_major_ticks)), 11)
        ]
    )
    fig, ax = chart.plt_2Dgraph()
    fig.set_size_inches(10, 10)
    plt.savefig(fn, dpi=300, bbox_inches="tight", pad_inches=1)

    os.remove(outdata_file)
    tk.messagebox.showinfo("showinfo", "Execution completed.")
